import torch

import numpy as np
import torch.nn as nn

from typing import *
from cfdata.tabular import TabularData
from sklearn.tree import _tree, DecisionTreeClassifier

from ...bases import ModelBase
from ...misc.toolkit import *
from ...modules.blocks import *


def export_structure(tree):
    tree = tree.tree_

    def recurse(node, depth):
        feature_dim = tree.feature[node]
        if feature_dim == _tree.TREE_UNDEFINED:
            yield depth, -1, tree.value[node]
        else:
            threshold = tree.threshold[node]
            yield depth, feature_dim, threshold
            yield from recurse(tree.children_left[node], depth + 1)
            yield depth, feature_dim, threshold
            yield from recurse(tree.children_right[node], depth + 1)

    return tuple(recurse(0, 0))


@ModelBase.register("ndt")
class NDT(ModelBase):
    def __init__(self,
                 config: Dict[str, Any],
                 tr_data: TabularData,
                 device: torch.device):
        super().__init__(config, tr_data, device)
        # prepare
        x, y = tr_data.processed.xy
        y_ravel, num_classes = y.ravel(), tr_data.num_classes
        x_tensor = torch.from_numpy(x).to(device)
        split_result = self._split_features(x_tensor)
        # decision tree
        self.log_msg("fitting decision tree", self.info_prefix, verbose_level=2)
        x_merge = split_result.merge().cpu().numpy()
        self.dt = DecisionTreeClassifier(**self.dt_config, random_state=142857).fit(x_merge, y_ravel)
        tree_structure = export_structure(self.dt)
        # dt statistics
        num_leafs = sum([1 if pair[1] == -1 else 0 for pair in tree_structure])
        num_internals = num_leafs - 1
        msg = f"internals : {num_internals} ; leafs : {num_leafs}"
        self.log_msg(msg, self.info_prefix, verbose_level=2)
        # transform
        b = np.zeros(num_internals, dtype=np.float32)
        w1 = np.zeros([self.merged_dim, num_internals], dtype=np.float32)
        w2 = np.zeros([num_internals, num_leafs], dtype=np.float32)
        w3 = np.zeros([num_leafs, num_classes], dtype=np.float32)
        node_list, node_sign_list = [], []
        node_id_cursor = leaf_id_cursor = 0
        for depth, feat_dim, rs in tree_structure:
            if feat_dim != -1:
                if depth == len(node_list):
                    node_sign_list.append(-1)
                    node_list.append(node_id_cursor)
                    w1[feat_dim, node_id_cursor] = 1
                    b[node_id_cursor] = -rs
                    node_id_cursor += 1
                else:
                    node_list = node_list[:depth + 1]
                    node_sign_list = node_sign_list[:depth] + [1]
            else:
                for node_id, node_sign in zip(node_list, node_sign_list):
                    w2[node_id, leaf_id_cursor] = node_sign / len(node_list)
                w3[leaf_id_cursor] = rs / np.sum(rs)
                leaf_id_cursor += 1
        w1, w2, w3, b = map(torch.from_numpy, [w1, w2, w3, b])
        # construct planes & routes
        self.to_planes = Linear(self.merged_dim, num_internals, init_method=None)
        self.to_routes = Linear(num_internals, num_leafs, bias=False, init_method=None)
        self.to_leafs = Linear(num_leafs, num_classes, init_method=None)
        with torch.no_grad():
            self.to_planes.linear.bias.data = b
            self.to_planes.linear.weight.data = w1.t()
            self.to_routes.linear.weight.data = w2.t()
            self.to_leafs.linear.weight.data = w3.t()
            uniform = nn.functional.log_softmax(torch.zeros(num_classes, dtype=torch.float32), dim=0)
            self.to_leafs.linear.bias.data = uniform

    @property
    def hyperplane_weights(self) -> np.ndarray:
        return to_numpy(self.to_planes.linear.weight)

    @property
    def hyperplane_thresholds(self) -> np.ndarray:
        return to_numpy(-self.to_planes.linear.bias)

    @property
    def route_weights(self) -> np.ndarray:
        return to_numpy(self.to_routes.linear.weight)

    @property
    def class_log_distributions(self) -> np.ndarray:
        return to_numpy(self.to_leafs.linear.weight)

    @property
    def class_log_prior(self) -> np.ndarray:
        return to_numpy(self.to_leafs.linear.bias)

    @property
    def class_prior(self) -> np.ndarray:
        return np.exp(self.class_log_prior)

    def _preset_config(self,
                       tr_data: TabularData):
        self.config.setdefault("default_encoding_method", "one_hot")

    def _init_config(self,
                     tr_data: TabularData):
        super()._init_config(tr_data)
        self.dt_config = self.config.setdefault("dt_config", {})
        activation_configs = self.config.setdefault("activation_configs", {})
        activation_configs.setdefault("multiplied_tanh", {}).setdefault("ratio", 10.)
        activation_configs.setdefault("multiplied_softmax", {}).setdefault("ratio", 10.)
        default_activations = {"planes": "sign", "routes": "multiplied_softmax"}
        activations = self.config.setdefault("activations", default_activations)
        activations_ins = Activations(activation_configs)
        self.planes_activation = activations_ins.module(activations.get("planes"))
        self.routes_activation = activations_ins.module(activations.get("routes"))
        self._init_with_dt = self.config.setdefault("")

    def forward(self,
                batch: tensor_dict_type,
                **kwargs) -> tensor_dict_type:
        x_batch = batch["x_batch"]
        merged = self._split_features(x_batch).merge()
        planes = self.planes_activation(self.to_planes(merged))
        routes = self.routes_activation(self.to_routes(planes))
        leafs = self.to_leafs(routes)
        return {"predictions": leafs}


__all__ = ["NDT"]
