# Copyright (c) ZOZO Technologies, Inc. All rights reserved.
# Licensed under the Apache 2.0 License.

"""Offline Bandit Simulator."""
from tqdm import tqdm

import numpy as np

from obp.dataset import BanditFeedback
from obp.policy import BanditPolicy


def run_bandit_simulation(bandit_feedback: BanditFeedback, policy: BanditPolicy) -> np.ndarray:
    """Run bandit algorithm on logged bandit feedback data.

    Parameters
    ----------
    bandit_feedback: BanditFeedback
        Logged bandit feedback data to be used in offline bandit simulation.

    policy: BanditPolicy
        Bandit policy to be used evaluated in offline bandit simulation (i.e., counterfactual or evaluation policy).

    Returns
    --------
    selected_actions: array-like shape (n_rounds, len_list)
        Lists of actions selected by counterfactual (or evaluation) policy at each round in offline bandit simulation.

    """
    _check_bandit_feedback(bandit_feedback=bandit_feedback)

    policy_ = policy
    selected_actions_list = list()
    dim_context = bandit_feedback['context'].shape[1]
    for action_, reward_, position_, pscore_, context_ in\
            tqdm(
                zip(
                    bandit_feedback['action'],
                    bandit_feedback['reward'],
                    bandit_feedback['position'],
                    bandit_feedback['pscore'],
                    bandit_feedback['context']
                ),
            total=bandit_feedback['n_rounds']
            ):

        # select a list of actions
        if policy_.policy_type == 'contextfree':
            selected_actions = policy_.select_action()
        elif policy_.policy_type == 'contextual':
            selected_actions = policy_.select_action(context_.reshape(1, dim_context))
        action_match_ = action_ == selected_actions[position_]
        # update parameters of a bandit policy
        # only when selected actions&positions are equal to logged actions&positions
        if action_match_:
            if policy_.policy_type == 'contextfree':
                policy_.update_params(action=action_, reward=reward_)
            elif policy_.policy_type == 'contextual':
                policy_.update_params(action=action_, reward=reward_, context=context_.reshape(1, dim_context))
        selected_actions_list.append(selected_actions)

    return np.array(selected_actions_list)


def _check_bandit_feedback(bandit_feedback: BanditFeedback) -> RuntimeError:
    """Check keys of input BanditFeedback dict."""
    for key_ in ['action', 'position', 'reward', 'pscore', 'context']:
        if key_ not in bandit_feedback:
            raise RuntimeError(f"Missing key of {key_} in 'bandit_feedback'.")
