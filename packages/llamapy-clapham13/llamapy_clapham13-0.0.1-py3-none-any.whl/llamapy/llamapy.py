import os # need to set these to allow Airpy to work
os.environ['ENABLE_EMR_HIVE'] = '1'
os.environ['EMR_CLUSTER'] = 'ml-infra-fireworks'
os.environ['CDH_METASTORE_CLUSTER'] = 'silver'

import airpy as ap
import datetime as dt
import gspread as gsp
import pandas as pd
import numpy as np

gc = gsp.service_account(filename='credentials/creds.json')

class Spreadsheet:
    
    def get_link(self, obj):
        from IPython.core.display import display, HTML
        _class = type(self).__name__.lower()
        if _class == 'spreadsheet':
            obj = obj.url
        text = 'Here\'s a <a href={}>link to your '+'{}</a>.'.format(_class)
        display(HTML(text.format(obj)))
    
    def __init__(self, title, shared_with):
        assert type(title)==str, 'Spreadsheet title must be a string'
        self.title = title
        self.shared_with = shared_with
        
        # try to open, otherwise create a new spreadsheet
        try:
            self.sh = gc.open(self.title)
        except:
            print('...creating a new spreadsheet...')
            self.sh = gc.create(self.title)
            try:
                self.sh.share(self.shared_with, 
                              perm_type='user', 
                              role='writer')
            except:
                print('please add an email or list of emails for file sharing')
        self.get_link(self.sh)
    
    def show_worksheets(self):
        return self.sh.worksheets()
    
    def share_with(self, email):
        self
        self.sh.share(email, perm_type='user', role='writer')
        
        
class Worksheet(Spreadsheet):
    
    def get_cell_range(self, range_type='dataframe'):
        n_rows = len(self.df)
        n_cols = len(self.df.columns)
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        col_alphas = [i for i in alpha] + [j+i for j in alpha for i in alpha]

        # calculate the range for the given df
        start_col = col_alphas[self.col_offset]
        start_row = self.row_offset + 1
        end_col = col_alphas[self.col_offset + n_cols - 1]
        end_row = n_rows + start_row

        # return full range if header==False, otherwise just return header row
        if range_type == 'dataframe':
            return '{}{}:{}{}'.format(start_col, start_row, end_col, end_row)
        elif range_type == 'header':
            return '{}{}:{}{}'.format(start_col, start_row, end_col, start_row)
        elif range_type == 'whole_sheet':
            return 'A1:{}{}'.format(col_alphas[self.col_offset + n_cols], 
                                    end_row + 3)
    
    
    def __init__(self, Spreadsheet, title, df, blank_sheet=False, 
                 row_offset=3, col_offset=1, title_text='',
                 title_color='rausch', header_text_color='white',
                 header_background_color='kazan', border_color='hof',
                 text_color='hof', font_style='Proxima Nova'
                ):
        self.parent_sheet = Spreadsheet.sh
        self.title = title
        self.df = df
        self.title_color = title_color
        self.header_text_color = header_text_color
        self.header_background_color = header_background_color
        self.border_color = border_color
        self.font_style = font_style
        self.text_color = text_color
        self.row_offset = row_offset
        self.col_offset = col_offset
        self.n_rows = len(df) + row_offset + 3
        self.n_cols = len(df.columns) + col_offset + 1
        self.df_cell_range = self.get_cell_range()
        self.header_range = self.get_cell_range(range_type='header')
        self.full_cell_range = self.get_cell_range(range_type='whole_sheet')
        self.ds_last_updated = dt.date.today().strftime('%b %d, %Y')
        
        # open worksheet or create if it doesn't exist
        try:
            self.worksheet = self.parent_sheet.add_worksheet(title=title, 
                                                             rows=self.n_rows, 
                                                             cols=self.n_cols)
        except:
            self.worksheet = self.parent_sheet.worksheet(title)
        
        # perform transformations on certain field-types in prep for upload
        for col in df.columns:
            _iter = 0
            NoneType = type(None)
            acceptable = (np.int64, np.float64, str, float, NoneType)
            
            try:
                _bool = type(df[col].sort_values().iloc[0]) not in acceptable
            except TypeError:              # for when sorting throws an error
                _bool = type(df[col].iloc[0]) not in acceptable
                
            if _bool:
                if _iter==0:
                    print('converting the following columns to string format:')
                    _iter+=1
                print('  {}'.format(col))
                df[col] = df[col].astype(str)

            # fill columns that have blanks (required for sheets to read file)
            if (df[col].value_counts().sum() >= 1) \
                & (df[col].value_counts().sum() < len(df)):
                df[col].fillna('', inplace=True)
        
        # insert data from dataframe
        self.worksheet.update(
            self.df_cell_range, [self.df.columns.values.tolist()] \
                        + self.df.values.tolist()
        )
        
        # add a filter, cause they're cool
        self.worksheet.set_basic_filter(self.df_cell_range)
        
        ### FORMATTING ###
        self.color_options = ['rausch','kazan','hackberry',
                              'beach','hof','white']
        rausch = {"red": 255.0/255, "green": 90.0/255, "blue": 95.0/255}
        kazan = {"red": 0.0/255, "green": 122.0/255, "blue": 135.0/255}
        hackberry = {"red": 123.0/255, "green": 0.0/255, "blue": 81.0/255}
        beach = {"red": 255.0/255, "green": 180.0/255, "blue": 0.0/255}
        hof = {"red": 86.0/255, "green": 90.0/255, "blue": 92.0/255}
        white = {"red": 1.0, "green": 1.0, "blue": 1.0}
        
        color_dict = {
            'rausch': rausch,
            'kazan': kazan,
            'hackberry': hackberry,
            'beach': beach,
            'hof': hof,
            'white': white
        }
        
        title_color = color_dict[title_color]
        header_text_color = color_dict[header_text_color]
        header_background_color = color_dict[header_background_color]
        border_color = color_dict[border_color]
        text_color = color_dict[text_color]
        
        ### make all borders blank
        border_style = {
            "style": "SOLID",
            "color": white
        }
        self.worksheet.format(self.full_cell_range, {
            "verticalAlignment":'MIDDLE',
            "borders": {
                "top": border_style,
                "bottom": border_style,
                "left": border_style,
                "right": border_style
            },
            "textFormat": {
                "fontSize": 9,
                "fontFamily": 'Proxima Nova',
            }
        })
        
        ### put hof-colored border around data
        border_style = {
            "style": "SOLID",
            "color": border_color
        }
        self.worksheet.format(self.df_cell_range, {
            "wrapStrategy": "WRAP",
            "horizontalAlignment": "CENTER",
            "borders": {
                "top": border_style,
                "bottom": border_style,
                "left": border_style,
                "right": border_style
            },
            "textFormat": {
                "fontSize": 9,
                "foregroundColor": text_color,
                "fontFamily": font_style,
            }
        })
        
        # format header range
        self.worksheet.format(self.header_range, {
            "backgroundColor": header_background_color,
            "horizontalAlignment": "CENTER",
            "textFormat": {
              "foregroundColor": header_text_color,
              "fontSize": 9,
              "fontFamily": font_style,
              "bold": True
            }
        })
        
        # add a title, if there's room at the top
        def get_title_cell(row_offset=self.row_offset, 
                           col_offset=self.col_offset):
            # finds where a title cell should be, if necessary
            alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            col = alpha[col_offset]

            if row_offset >= 3:
                row = (row_offset + 1) // 2
                return '{}{}'.format(col, row)
            elif row_offset >= 1:
                return '{}{}'.format(col, 1)
            else:                                # no title if offset is 0
                print('couldn\'t add a title cell due to specified offset')
                return False
            
        title_cell = get_title_cell()
        if title_text == '':
            self.title_text = self.title
        else:
            self.title_text = title_text
        
        if title_cell != False:
            self.worksheet.update(title_cell, self.title_text)
            self.worksheet.format(title_cell, {
                "textFormat": {
                  "foregroundColor": title_color,
                  "fontSize": 16,
                  "fontFamily": font_style,
                  "bold": True
                }
            })
            merge_cell = get_title_cell(col_offset=self.col_offset+3)
            self.worksheet.merge_cells('{}:{}'.format(title_cell, merge_cell))
            if self.row_offset >=2: 
                sub_title_cell = get_title_cell(row_offset=self.row_offset+2)
                sub_title_text = 'data pulled: {}'.format(self.ds_last_updated)
                self.worksheet.update(sub_title_cell, sub_title_text)
                self.worksheet.format(sub_title_cell, {
                    "verticalAlignment":'TOP',
                    "textFormat": {
                      "foregroundColor": hof,
                      "fontSize": 8,
                      "fontFamily": 'Proxima Nova',
                    }
                })
        
        # returns a link
        self.url = self.parent_sheet.url + '#gid=' + str(self.worksheet.id)
        self.get_link(self.url)


def get_lp(days_ago=1):
    lp = dt.datetime.today() - dt.timedelta(days_ago)
    lp = lp.date()
    return '{:04}-{:02}-{:02}'.format(lp.year, lp.month, lp.day)
        
def convert_lps(presto_query):
    _iter = 0
    while (presto_query.find('{{') >= 0) & (_iter < 200):
        start = presto_query.find('{{')
        end = presto_query.find('}}')
        presto_query = presto_query.replace(presto_query[start+1:end+1],'lp')
        _iter+=1 # just to prevent infinite loops
    
    return presto_query
