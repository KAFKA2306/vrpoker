import json
from copy import deepcopy
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
class RulesBuilder():
    """
    two card texas holdem game tree builder
    """
    def __init__(self,
                 rule,
                 current_commit = [2,2],
                 current_round =  2,
                 raise_limit = 1,
                 check_limit = 2,
                 small_blind = 0.5,
                 big_blind = 1,
                 stack = 10,
                 bet_sizes = ["1_pot"],
                 raise_sizes = ["1_pot"],
                 allin_threshold = 0.67,
                 ):
        self.rule = rule
        self.parse_rules()
        self.current_commit = current_commit
        self.current_round = current_round
        self.raise_limit = raise_limit
        self.check_limit = check_limit
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.stack = stack
        self.bet_sizes = bet_sizes
        self.raise_sizes = raise_sizes
        self.allin_threshold = allin_threshold
        self.initial_effective_stack = stack - self.current_commit[0]
    def parse_rules(self):
        for k,v in self.rule.items():
            setattr(self,k,v)
        rule = Struct(**self.rule)
        self.rule = rule
    def get_beginning_chip(self):
        assert(self.players >= 2)
        midbets = []
        for i in range(self.players - 2):
            midbets.append(0)
        chips = [self.small_blind] + midbets + [self.big_blind]
        return chips
def raise_number_this_round(root):
    if root is None:
        return 0
    elif not isinstance(root,ActionNode):
        return 0
    elif isinstance(root,DealCardNode):
        return 0
    elif 'raise' in root.last_action:
        return 1 + raise_number_this_round(root.parent)
    elif 'raise' not in root.last_action:
        return raise_number_this_round(root.parent)
    elif root.last_action == 'begin':
        return 0
    else:
        raise
def check_number_this_round(root):
    if root is None:
        return 0
    elif not isinstance(root,ActionNode):
        return 0
    elif isinstance(root,DealCardNode):
        return 0
    elif 'check' in root.last_action:
        return 1 + check_number_this_round(root.parent)
    elif 'check' not in root.last_action:
        return check_number_this_round(root.parent)
    elif root.last_action == 'begin':
        return 0
    else:
        raise
class TreeBuilder:
    def __init__(self,rule):
        self.rule = rule
        self.build_tree()
    def build_tree(self):
        pass
    def format_tree(self,depth_limit=None):
        self.formatted_arr = []
        formatted_arr = self.formatted_arr
        self.__format_tree(self.root,1,depth_limit)
        return formatted_arr
    def plot_tree(self,jupyter=True,depth_limit = 50,show=False):
        assert jupyter
        tree_tovis = self.format_tree(depth_limit=depth_limit)
        G = nx.DiGraph()
        for t in tree_tovis:
            G.add_edge(t[0], t[1])
        pos=graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True, arrows=False)
        if show:
            plt.show()
    def __format_tree(self,root,depth,limit):
        if limit is not None and depth > limit:
            return
        if root.children is not None:
            for one_child in root.children.values():
                self.formatted_arr.append([root.to_string(),one_child.to_string()])
                self.__format_tree(one_child,depth + 1,limit)
    def gen_km_json(self,json_file,path_prefix=[],limit=np.inf,ret_json=False):
        """
        利用百度脑图的格式可视化决策树
        """
        root = self.root
        for one_action in path_prefix:
            root = root.children[one_action]
        retjson = self.__gen_km_json(root,depth = 0,limit=limit)
        with open(json_file,'w') as whdl:
            json.dump({'root':retjson},whdl)
        if ret_json == True:
            return retjson
    def __gen_km_json(self,root,depth,limit,parent=None):
        if limit is not None and depth > limit:
            return
        children = []
        children_actions = []
        text = root.to_string()
        node_type = "Action"
        if "dealcard" in text and "dealcard" in parent.to_string():
            text = "Chance [DealCard]"
        text += "\nround: {}".format({1:"preflop",2:"flop",3:"turn",4:"river"}[root.betting_round])
        if "dealcard" in text and "dealcard" not in parent.to_string():
            node_type = "Chance"
        if root.terminal == True:
            node_type = "Terminal"
        elif root.showdown == True:
            if root.betting_round == 4:
                node_type = "Showdown"
            else:
                node_type = "Chance"
        one_json = {
            "data": {
                "text": text},
            "children": children,
            "children_actions": children_actions,
            "font-weight": "bold",
            "background": "
            "resource": [],
            "meta":{
                "round": {1:"preflop",2:"flop",3:"turn",4:"river"}[root.betting_round],
                "player": root.player,
                "pot":root.pot,
                "node_type":node_type
            }
        }
        if root.showdown == True:
            one_json["meta"]["payoffs"] = root.payoffs
        elif root.terminal == True:
            one_json["meta"]["payoff"] = root.payoff
        if root.children is not None:
            if node_type == "Chance":
                root_childs = [["dealcard",root]]
            else:
                root_childs = root.children.items()
            for one_action,one_child in root_childs:
                child_json = self.__gen_km_json(one_child,depth + 1,limit,root)
                if child_json:
                    children.append(child_json)
                    children_actions.append(one_action)
        if root.showdown == True and root.betting_round < 4:
            one_json["meta"]["node_type"] = node_type
            one_json["meta"]["round"] = {1:"preflop",2:"flop",3:"turn",4:"river"}[root.betting_round + 1]
            text = "Chance [DealCard]\nround:{}".format(one_json["meta"]["round"])
            one_json["data"]["text"] = text
            new_root = deepcopy(root)
            new_root.betting_round += 1
            child_json = self.__gen_km_json(new_root,depth + 1,limit,root)
            children.append(child_json)
            children_actions.append("dealcard")
        return one_json
class FiveCardTexasTreeBuilder(TreeBuilder):
    def build_tree(self):
        players = list(range(self.rule.players))
        player = 0
        root = ActionNode(None,committed = self.rule.get_beginning_chip(),players = players,player = player,last_action='begin',bet_history = [],betting_round=1)
        self.root = root
        return self.__build(root)
    def __build(self,root):
        if type(root) is ActionNode:
            self.build_action(root)
        elif type(root) is ShowdownNode:
            pass
        elif type(root) is TerminalNode:
            pass
        elif type(root) is DealCardNode:
            self.build_action(root)
        else:
            print(type(root),' should not be a node type')
            raise
        return root
    def get_possible_betting_sizes(self,root,player,next_player,typeofbet,rule):
        committed = root.committed
        if typeofbet == "bet":
            illegal_bets = self.rule.bet_sizes
        elif typeofbet == "raise":
            illegal_bets = self.rule.raise_sizes
        else:
            raise
        bets = []
        for one_bet in illegal_bets:
            assert('_pot' in one_bet or one_bet == "all-in")
            if '_pot' in one_bet:
                one_bet = one_bet.replace("_pot","")
                one_bet = float(one_bet)
            elif 'all-in' == one_bet:
                pass
            bets.append(one_bet)
        pot = max(committed) * 2
        possible_amounts = []
        def round_nearest(number,round_num):
            round_num = 1 / round_num
            return round((number * round_num)) / round_num
        sb = self.rule.small_blind
        bb = self.rule.big_blind
        for one_bet in bets:
            if type(one_bet) is float or type(one_bet) is int:
                if committed[player] == sb:
                    amount = one_bet * committed[next_player]  - sb
                    amount = round_nearest(amount,sb)
                elif committed[player] == bb and committed[next_player] == bb:
                    amount = one_bet * bb
                    amount = round_nearest(amount,sb)
                else:
                    amount = one_bet * pot
                    amount = round_nearest(amount,bb)
                if typeofbet == "raise":
                    amount += (committed[next_player] - committed[player])
                if amount + committed[player] > rule.initial_effective_stack * rule.allin_threshold:
                    amount = -1
            elif type(one_bet) == str:
                assert(one_bet == 'all-in')
                amount = self.rule.stack - committed[player]
            if amount > 0:
                possible_amounts.append(amount)
        if committed[player] != sb:
            possible_amounts = [int(i) for i in possible_amounts if i > 0]
        if committed[player] == sb:
            possible_amounts = [i for i in possible_amounts if i >= bb]
        elif committed[player] == bb and committed[next_player] == bb:
            possible_amounts = [i for i in possible_amounts if i >= bb]
        else:
            gap = committed[next_player] - committed[player]
            assert(gap >= 0)
            possible_amounts = [i for i in possible_amounts if i >= gap * 2]
            possible_amounts = [i for i in possible_amounts if i <= self.rule.stack - committed[player]]
        return possible_amounts
    def build_action(self,root):
        players = root.players
        player = root.player
        if type(root) is DealCardNode:
            possible_actions = self.rule.legal_actions_after['roundbegin']
        else:
            possible_actions = self.rule.legal_actions_after[root.last_action.split('_')[0]]
        next_player = (player + 1) % len(players)
        if possible_actions is None:
            return
        check_limit = self.rule.check_limit
        checksum = check_number_this_round(root)
        for one_action in possible_actions:
            if one_action == 'check':
                committed = deepcopy(root.committed)
                if (root.last_action == 'call' and root.betting_round == 1) or checksum >= check_limit - 1:
                    if root.betting_round == self.rule.rounds:
                        nextnode = ShowdownNode(root,committed = committed,players = players,player = next_player,last_action=one_action,bet_history = root.bet_history + [one_action])
                    else:
                        nextnode = DealCardNode(root,committed = committed,players = players,player = 1,last_action=one_action,bet_history = root.bet_history + [one_action],betting_round=root.betting_round + 1)
                elif root.parent is not None:
                    nextnode = ActionNode(root,committed = committed,players = players,player = next_player,last_action=one_action,bet_history = root.bet_history + [one_action])
                else:
                    nextnode = ActionNode(root,committed = committed,players = players,player = next_player,last_action=one_action,bet_history = root.bet_history + [one_action])
                self.__build(nextnode)
            elif one_action == 'bet':
                betting_sizes = self.get_possible_betting_sizes(root,player,next_player,"bet",self.rule)
                for one_betting_size in betting_sizes:
                    committed = deepcopy(root.committed)
                    committed[player] += one_betting_size
                    one_action_bet = one_action + "_" + str(one_betting_size)
                    nextnode = ActionNode(root,committed = committed,players = players,player = next_player,last_action=one_action_bet,bet_history = root.bet_history + [one_action_bet])
                    self.__build(nextnode)
            elif one_action == 'call':
                committed = deepcopy(root.committed)
                committed[player] += committed[next_player] - committed[player]
                if root.last_action == 'begin':
                    nextnode = ActionNode(root,committed = committed,players = players,player = next_player,last_action=one_action,bet_history = root.bet_history + [one_action])
                elif root.betting_round == self.rule.rounds or np.any(self.rule.stack - np.asarray(root.committed) <= 0):
                    nextnode = ShowdownNode(root,committed = committed,players = players,player = next_player,last_action=one_action,bet_history = root.bet_history + [one_action])
                else:
                    nextnode = DealCardNode(root,committed = committed,players = players,player = 1,last_action=one_action,bet_history = root.bet_history + [one_action],betting_round = root.betting_round + 1)
                self.__build(nextnode)
            elif one_action == 'raise':
                if root.last_action == 'call':
                    if root.parent and root.parent.parent is None:
                        pass
                    else:
                        continue
                if root.last_action == 'check':
                    if root.parent and (root.parent.parent is None and root.betting_round == 1):
                        pass
                    else:
                        continue
                if raise_number_this_round(root) >= self.rule.raise_limit:
                    continue
                betting_sizes = self.get_possible_betting_sizes(root,player,next_player,"raise",self.rule)
                for one_betting_size in betting_sizes:
                    one_action_raise = one_action + "_" + str(one_betting_size)
                    committed = deepcopy(root.committed)
                    committed[player] += one_betting_size
                    nextnode = ActionNode(root,committed = committed,players = players,player = next_player,last_action=one_action_raise,bet_history = root.bet_history + [one_action_raise])
                    self.__build(nextnode)
            elif one_action  == 'fold':
                committed = deepcopy(root.committed)
                nextnode = TerminalNode(root,committed = committed,players = players,player = next_player,last_action=one_action,bet_history = root.bet_history + [one_action])
                self.__build(nextnode)
            else:
                raise
class PartGameTreeBuilder(FiveCardTexasTreeBuilder):
    def __init__(self,rule):
        self.rule = rule
        self.build_tree()
    def build_tree(self):
        players = list(range(self.rule.players))
        player = self.rule.current_player
        current_round = self.rule.current_round
        root = ActionNode(None,committed = self.rule.current_commit,players = players,player = player,last_action='roundbegin',bet_history = [],betting_round=current_round)
        self.root = root
        return self.__build(root)
    def __build(self,root):
        if type(root) is ActionNode:
            self.build_action(root)
        elif type(root) is ShowdownNode:
            pass
        elif type(root) is TerminalNode:
            pass
        elif type(root) is DealCardNode:
            self.build_action(root)
        else:
            print(type(root),' should not be a node type')
            raise
        return root
class Node(object):
    def __init__(self, parent, committed, players, player,  bet_history,betting_round=None,**kwargs):
        self.committed = deepcopy(committed)
        self.pot = sum(committed)
        self.bet_history = deepcopy(bet_history)
        self.players = players
        self.player = player
        self.children = None
        self.parent = parent
        self.terminal = False
        self.showdown = False
        self.serialized = None
        self.betting_round = betting_round if betting_round is not None else (parent.betting_round if parent is not None else None)
    def get_opponent(self):
        if len(self.players) == 2:
            return (self.player + 1) % len(self.players)
        else:
            return list(set(self.players) - set([self.player,]))
    def add_child(self, child):
        if self.children is None:
            self.children = [child]
        else:
            self.children.append(child)
    def serialize(self):
        if self.serialized is None:
            self.serialized =  "[{}]".format("|".join(self.bet_history))
        return self.serialized
    def to_string(self):
        return "{}\n{} \n {}".format(
            "player: " + str(self.get_opponent()),
            "pot:" + "-".join([str(i) for i in self.committed]),
            hash(''.join(self.bet_history)) % 10000
        )
class ChanceNode(Node):
    def __init__(self, parent, committed, players, player,  bet_history,betting_round=None,**kwargs):
        super().__init__(parent, committed, players, player,  bet_history,betting_round=betting_round)
        self.last_action = kwargs['last_action']
        if parent:
            self.parent.add_child(self,self.last_action)
    def add_child(self, child,action):
        if self.children is None:
            self.children = { action:child }
        else:
            self.children[action] = child
    def to_string(self):
        return "{}-{}\n{} \n {}".format(
            "player: " + str(self.get_opponent()),
            self.last_action,
            "pot:" + "-".join([str(i) for i in self.committed]),
            hash(''.join(self.bet_history)) % 10000
        )
class ActionNode(Node):
    def __init__(self, parent, committed, players, player,  bet_history,betting_round=None,**kwargs):
        super().__init__(parent, committed, players, player,  bet_history,betting_round=betting_round)
        self.last_action = kwargs['last_action']
        if parent:
            self.parent.add_child(self,self.last_action)
    def add_child(self, child,action):
        if self.children is None:
            self.children = { action:child }
        else:
            self.children[action] = child
    def to_string(self):
        return "{}-{}\n{} \n {}".format(
            "player: " + str(self.get_opponent()),
            self.last_action,
            "pot:" + "-".join([str(i) for i in self.committed]),
            hash(''.join(self.bet_history)) % 10000
        )
class ShowdownNode(ActionNode):
    def __init__(self, parent, committed, players, player,  bet_history,betting_round=None,**kwargs):
        super().__init__(parent, committed, players, player,  bet_history,betting_round=betting_round, ** kwargs)
        self.last_action = kwargs['last_action']
        if parent:
            self.parent.add_child(self,self.last_action)
        self.payoffs = {}
        for i in players:
            self.payoffs[i] = [-i for i in self.committed]
            self.payoffs[i][i] += self.pot
        self.payoffs['tie'] = [-i + (self.pot / 2) for i in self.committed]
        self.showdown = True
    def add_child(self, child,action):
        raise
    def to_string(self):
        return "{}\n{}-{}\n{} \n {} \n {}".format(
            "[++showdown++]",
            "player: " + str(self.get_opponent()),
            self.last_action,
            "pot:" + "-".join([str(i) for i in self.committed]),
            self.payoffs,
            hash(''.join(self.bet_history)) % 10000,
            )
class DealCardNode(ShowdownNode):
    def __init__(self, parent, committed, players, player,  bet_history,betting_round=None,**kwargs):
        super().__init__(parent, committed, players, player,  bet_history,betting_round=betting_round, ** kwargs)
        self.showdown = False
    def add_child(self, child,action):
        if self.children is None:
            self.children = { action:child }
        else:
            self.children[action] = child
    def to_string(self):
        return "{}\n{}-{}\n{} \n {} \n {}".format(
            "[++dealcard++]",
            "player: " + str(self.get_opponent()),
            self.last_action,
            "pot:" + "-".join([str(i) for i in self.committed]),
            self.payoffs,
            hash(''.join(self.bet_history)) % 10000,
            )
class TerminalNode(ActionNode):
    def __init__(self, parent, committed, players, player,  bet_history,betting_round=None,**kwargs):
        super().__init__(parent, committed, players, player,  bet_history,betting_round=betting_round, ** kwargs)
        self.last_action = kwargs['last_action']
        if parent:
            self.parent.add_child(self,self.last_action)
        self.payoff = []
        self.payoff = [-i for i in self.committed]
        self.payoff[player] += self.pot
        self.terminal = True
    def add_child(self, child,action):
        raise
    def to_string(self):
        return "{}\n{}-{}\n{} \n {} \n {}".format(
            "[--terminal--]",
            "player: " + str(self.get_opponent()),
            self.last_action,
            "pot:" + "-".join([str(i) for i in self.committed]),
            self.payoff,
            hash(''.join(self.bet_history)) % 10000,
            )
class HolecardChanceNode(Node):
    def __init__(self, parent, committed, holecards, board, deck, bet_history, todeal):
        Node.__init__(self, parent, committed, holecards, board, deck, bet_history)
        self.todeal = todeal
        self.children = []
class BoardcardChanceNode(Node):
    def __init__(self, parent, committed, holecards, board, deck, bet_history, todeal):
        Node.__init__(self, parent, committed, holecards, board, deck, bet_history)
        self.todeal = todeal
        self.children = []
