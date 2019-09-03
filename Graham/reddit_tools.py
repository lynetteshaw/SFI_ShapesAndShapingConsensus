import pandas as pd
import numpy as np
import os
import datetime

def import_csv_as_df(filename):
    df = pd.read_csv(filename)
    
    # make a new field with easier datetime, remove old field with utc format
    df['OPcreatedAt'] = pd.to_datetime(df['op_created_utc'], unit = 's')
    df = df.drop(columns=['op_created_utc'])
    df['createdAt'] = pd.to_datetime(df['created_utc'], unit = 's')
    df = df.drop(columns=['created_utc'])


    # remove data from before Election (Nov 9, 2016)
    election_date = '2016-11-09 00:00:00'
    df = df[df['createdAt']>election_date]

    # Remove all columns that are all NaN
    return df[df.columns[~pd.isna(df).all()]]
    
    
def get_time_window(df, t_start,t_end):
    
    
    t_start_str = '-'.join(list(map(str, t_start))) + ' 00:00:00'
    t_end_str = '-'.join(list(map(str, t_end))) + ' 00:00:00'    
    
    return df[(df['createdAt']>=t_start_str) & 
              (df['createdAt']<t_end_str)]

def parse_df(df):
    id2post = {}
    users = {}
    for index, row in df.iterrows():
        # add comment to dictionary
        id2post[row['id']] = Comment(row)

        # add user to dictionary
        if row['author'] in users:
            users[row['author']].update_user(row)
        else:
            users[row['author']] = User(row)

def get_max_depth_below_post(comment_id, parent2children):
    # if you reach a leaf, stop, return zero
    children_depths = []
    if not parent2children[comment_id]:
        return 0
    else:
        for child_id in parent2children[comment_id]:
            children_depths.append(get_max_depth_below_post(child_id, parent2children))
        return np.max(children_depths) + 1

def count_total_nodes_below_post(comment_id, parent2children):
    # if you reach a leaf, stop, return zero
    if not parent2children[comment_id]:
        return 1
    else:
        child_list = []
        for child_id in parent2children[comment_id]:
            child_list.append(count_total_nodes_below_post(child_id, parent2children))
        return np.sum(child_list) + 1


class Comment:
    def __init__(self, row_df):

        # original post properties
        self.op_id = row_df['link_id']
        self.subreddit = row_df['subreddit']
        self.title = row_df['title']
        self.op_text = row_df['selftext']
        self.op_author = row_df['op_author']
        self.OPcreatedAt = row_df['OPcreatedAt']

        # comment properties
        self.id = row_df['id']
        self.score = row_df['score']
        self.author = row_df['author']
        self.body = row_df['body']
        self.controversiality = row_df['controversiality']
        self.createdAt = row_df['createdAt']

        # relationships of comment
        self.parent_id = row_df['parent_id'].split('_')[1]
        self.num_children = row_df['num_comments']
        self.child_comments = []
        self.total_descendant_number = 0
        #self.num_descendants = row_df['num_comments']

    def add_child(self, child_comment):
        self.child_comments.append(child_comment)

    def add_all_descendants(self, comment, parent2children, id2comment):
        self.total_descendant_number += len(parent2children[comment.id])
        for child_id in parent2children[comment.id]:
            child = id2comment[child_id]
            comment.add_child(child)
            comment.add_all_descendants(child, parent2children, id2comment)

    def get_child_comment_ids(self):
        return [child.id for child in self.child_comments]

    '''def get_all_descendant_ids(self):
        if not self.child_comments:
            return self.id
        
        for child_id in self.get_all_descendant_ids():'''




    

class OriginalPost(Comment):
    def __init__(self, op_id):
        # store id of original post
        self.id = op_id
        # initialize other fields to empty
        self.title = ''
        self.body = ''
        self.subreddit = ''
        self.author = ''
        self.createdAt = ''
        self.score = ''
        self.controversiality = ''
        self.child_comments = []
        self.num_children = 0
        self.num_descendants = 0
        self.all_discussion_authors = []
        self.total_descendant_number = 0

    def update_OP_stats(self):
        get_max_depth_below_post(op.id, parent2children)
        self.total_descendant_number = count_total_nodes_below_post(op.id, parent2children)




def get_list_tuple_tree_structure(top_node, parent2children):
    if not parent2children[top_node]:
        return []
    else:
        top_node.child_comments











        '''self.author = row_df['OPauthor']
        #self.score = row_df['OPscore']
        self.body = row_df['selftext']
        self.subreddit = row_df['subreddit']
        self.title = row_df['title']
        self.body = row_df['body']
        self.controversiality = row_df['controversiality']
        self.id = row_df['id']
        self.createdAt = row_df['OPcreatedAt']
        self.child_comments = []
        self.num_children = 0
        self.num_descendants = 0'''





class User:
    def __init__(self, row):

        # store ids of related comments
        self.comment_list = []
        self.responded_to = []

        # store related users
        self.user_responded_to = []

        # add info
        self.update_user(row)

    def update_user(self, row):
        self.comment_list.append(row['id'])
        self.responded_to.append(row['parent_id'].split('_')[1])

        #self.user_responded_to.append(row['id'])







# OP if linkID matchds OPID
