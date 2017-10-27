"""
Copyright (C) 2017 kanishka-linux kanishka.linux@gmail.com

This file is part of kawaii-player.

kawaii-player is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kawaii-player is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kawaii-player.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import sqlite3
import shutil
from PyQt5 import QtCore, QtWidgets
from player_functions import write_files, open_files, send_notification

class TitleListWidget(QtWidgets.QListWidget):
    
    def __init__(self, parent, uiwidget=None, home_var=None, tmp=None, logr=None):
        super(TitleListWidget, self).__init__(parent)
        global MainWindow, home, TMPDIR, logger, ui
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        MainWindow = parent
        ui = uiwidget
        TMPDIR = tmp
        home = home_var
        logger = logr

    def mouseMoveEvent(self, event): 
        if ui.auto_hide_dock and not ui.dockWidget_3.isHidden():
            ui.dockWidget_3.hide()
        self.setFocus()
    """
    def dropEvent(self, event):
        if (event.source() == self 
                and (event.dropAction() == QtCore.Qt.MoveAction 
                or self.dragDropMode() == QtWidgets.QAbstractItemView.InternalMove)):
            i = self.currentItem()
            item = i.text()
            itemR = self.currentRow()
            print("Mouse Release")
            print(item)
            p = self.itemAt(event.pos())
            m = p.text()
            n = self.row(p)
            print(n)
            print(itemR)
            if itemR != n:
                self.takeItem(itemR)
                del i
                self.insertItem(n, item)
                param_dict = ui.get_parameters_value(b='bookmark', o='opt', s='status')
                bookmark = param_dict['bookmark']
                opt = param_dict['opt']
                status = param_dict['status']
                if bookmark or opt == "History":
                    file_path = ""
                    if bookmark:
                        if os.path.exists(os.path.join(home, 'Bookmark', status+'.txt')):
                            file_path = os.path.join(home, 'Bookmark', status+'.txt')
                            l = open_files(file_path, True)
                            lines = []
                            for i in l:
                                i = re.sub('\n', '', i)
                                lines.append(i)
                                
                            if n > itemR:
                                t = lines[itemR]
                                i = itemR
                                while(i < n):
                                    lines[i] = lines[i+1]
                                    i = i+1
                                lines[n] = t
                            else:
                                i = itemR
                                t = lines[itemR]
                                while(i > n):
                                    lines[i] = lines[i-1]
                                    i = i -1
                                lines[n]=t
                            j = 0
                            length = len(lines)
                            write_files(file_path, lines, line_by_line=True)
                            self.clear()
                            for i in lines:
                                j = i.split(':')
                                self.addItem(j[-1])
                            self.setCurrentRow(n)
                    else:
                        param_dict = ui.get_parameters_value(s='site', sn='siteName')
                        site = param_dict['site']
                        siteName = param_dict['siteName']
                        if site == "SubbedAnime" or site == "DubbedAnime":
                            if os.path.exists(os.path.join(home, 'History', site, siteName, 'history.txt')):
                                file_path = os.path.join(home, 'History', site, siteName, 'history.txt')
                        else:
                            if os.path.exists(os.path.join(home, 'History', site, 'history.txt')):
                                file_path = os.path.join(home, 'History', site, 'history.txt')
                        write_files(file_path, ui.original_path_name, line_by_line=True)
                        self.setCurrentRow(n)
        else:
            QtWidgets.QListWidget.dropEvent(event)
    """
    
    def keyPressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_Left):
            self.set_search_backend(use_search='tmdb+ddg')
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_Right):
            self.set_search_backend(use_search='tvdb+ddg')
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_Down):
            self.set_search_backend(use_search='tmdb+g')
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_Up):
            self.set_search_backend(use_search='tvdb+g')
        elif (event.modifiers() == QtCore.Qt.AltModifier 
                and event.key() == QtCore.Qt.Key_1):
            self.set_search_backend(use_search=False)
        elif (event.modifiers() == QtCore.Qt.AltModifier 
                and event.key() == QtCore.Qt.Key_2):
            self.set_search_backend(use_search='tmdb')
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_A):
            self.get_all_information()
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_C):
            ui.copyFanart()
        elif (event.key() == QtCore.Qt.Key_F6):
            if self.currentItem():
                row = self.currentRow()
            else:
                row = 0
            if self.currentItem():
                mycopy = ui.epn_arr_list.copy()
                ui.metaengine.find_info_thread(0, row, mycopy)
        elif (event.key() == QtCore.Qt.Key_F7):
            if self.currentItem():
                row = self.currentRow()
            else:
                row = 0
            if self.currentItem():
                mycopy = ui.epn_arr_list.copy()
                ui.metaengine.find_info_thread(1, row, mycopy)
        elif (event.key() == QtCore.Qt.Key_F8):
            if self.currentItem():
                row = self.currentRow()
            else:
                row = 0
            if self.currentItem():
                mycopy = ui.epn_arr_list.copy()
                ui.metaengine.find_info_thread(2, row, mycopy)
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_Delete):
            row = self.currentRow()
            file_path = ""
            param_dict = ui.get_parameters_value(s='site', sn='siteName')
            site = param_dict['site']
            siteName = param_dict['siteName']
            if site == "SubbedAnime" or site == "DubbedAnime":
                if os.path.exists(os.path.join(home, 'History', site, siteName, 'history.txt')):
                    file_path = os.path.join(home, 'History', site, siteName, 'history.txt')
            else:
                if os.path.exists(os.path.join(home, 'History', site, 'history.txt')):
                    file_path = os.path.join(home, 'History', site, 'history.txt')
            if os.path.exists(file_path):
                row = self.currentRow()
                item = self.item(row)
                if item:
                    self.takeItem(row)
                    del item
                    del ui.original_path_name[row]
                    length = self.count()-1
                    write_files(file_path, ui.original_path_name, line_by_line=True)
        elif (event.modifiers() == QtCore.Qt.ShiftModifier 
                and event.key() == QtCore.Qt.Key_C):
            ui.copySummary()
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_B):
            param_dict = ui.get_parameters_value(b='bookmark', o='opt')
            bookmark = param_dict['bookmark']
            opt = param_dict['opt']
            if not bookmark:
                if opt != "History":
                    ui.listfound()
                param_dict = ui.get_parameters_value(
                    s='site', sn='siteName', bu='base_url', e='embed',
                    n='name', r='refererNeeded', f='finalUrlFound')
                site = param_dict['site']
                siteName = param_dict['siteName']
                base_url = param_dict['base_url']
                embed = param_dict['embed']
                name = param_dict['name']
                refererNeeded = param_dict['refererNeeded']
                finalUrlFound = param_dict['finalUrlFound']
                tmp = site+':'+"History"+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+finalUrlFound+':'+refererNeeded
                file_path = os.path.join(home, 'Bookmark', 'bookmark.txt')
                write_files(file_path, tmp, line_by_line=True)
                note = name + " is Bookmarked"
                send_notification(note, code=0)
        elif event.key() == QtCore.Qt.Key_PageUp:
            param_dict = ui.get_parameters_value(
                b='bookmark', s='site', o='opt', st='status', sn='siteName')
            bookmark = param_dict['bookmark']
            status = param_dict['status']
            opt = param_dict['opt']
            site= param_dict['site']
            siteName = param_dict['siteName']
            if bookmark:
                file_path = os.path.join(home, 'Bookmark', status+'.txt')
                if os.path.exists(file_path):
                    lins = open_files(file_path, True)
                    lines = []
                    for i in lins:
                        i = re.sub('\n', '', i)
                        lines.append(i)
                    r = self.currentRow()
                    length = self.count()
                    if r == 0:
                        p = length - 1
                    else:
                        p = r - 1
                    if length > 1:
                        t = lines[r]
                        lines[r] = lines[p]
                        lines[p] = t
                        write_files(file_path, lines, line_by_line=True)
                        self.clear()
                        ui.original_path_name[:] = []
                        for i in lines:
                            i = i.strip()
                            j = i.split(':')
                            if j[5].startswith('@'):
                                self.addItem(j[5].split('@')[-1])
                            elif '	' in j[5]:
                                k = j[5].split('	')[0]
                                self.addItem(k)	
                            else:
                                self.addItem(j[5])
                            ui.original_path_name.append(j[5])
                        self.setCurrentRow(p)
            elif opt == "History" and site!= "Music":
                file_path = ''
                if site == "SubbedAnime" or site == "DubbedAnime":
                    if os.path.exists(os.path.join(home, 'History', site, siteName, 'history.txt')):
                        file_path = os.path.join(home, 'History', site, siteName, 'history.txt')
                else:
                    if os.path.exists(os.path.join(home, 'History', site, 'history.txt')):
                        file_path = os.path.join(home, 'History', site, 'history.txt')
                row = self.currentRow()
                if row == 0:
                    prev_row = self.count()-1
                else:
                    prev_row = row - 1
                ui.original_path_name[row], ui.original_path_name[prev_row] = ui.original_path_name[prev_row], ui.original_path_name[row]
                if os.path.exists(file_path):
                    write_files(file_path, ui.original_path_name, line_by_line=True)
                self.clear()
                for i in ui.original_path_name:
                    if '	' in i:
                        i = i.split('	')[0]
                    self.addItem(i)
                self.setCurrentRow(prev_row)
        elif event.key() == QtCore.Qt.Key_PageDown:
            param_dict = ui.get_parameters_value(
                b='bookmark', s='site', o='opt', st='status', sn='siteName')
            bookmark = param_dict['bookmark']
            status = param_dict['status']
            opt = param_dict['opt']
            site= param_dict['site']
            siteName = param_dict['siteName']
            if bookmark:
                file_path = os.path.join(home, 'Bookmark', status+'.txt')
                if os.path.exists(file_path):
                    lins = open_files(file_path, True)
                    lines = []
                    for i in lins:
                        i = re.sub('\n', '', i)
                        lines.append(i)
                    r = self.currentRow()
                    length = self.count()
                    if r == length -1:
                        p = 0
                    else:
                        p = r + 1
                    if length > 1:
                        t = lines[r]
                        lines[r] = lines[p]
                        lines[p] = t
                        write_files(file_path, lines, line_by_line=True)
                        self.clear()
                        ui.original_path_name[:] = []
                        for i in lines:
                            i = re.sub('\n', '', i)
                            j = i.split(':')
                            if j[5].startswith('@'):
                                self.addItem(j[5].split('@')[-1])
                            elif '	' in j[5]:
                                k = j[5].split('	')[0]
                                self.addItem(k)
                            else:
                                self.addItem(j[5])
                            ui.original_path_name.append(j[5])
                        self.setCurrentRow(p)
            elif opt =="History" and site!= "Music":
                if site == "SubbedAnime" or site == "DubbedAnime":
                    if os.path.exists(os.path.join(home, 'History', site, siteName, 'history.txt')):
                        file_path = os.path.join(home, 'History', site, siteName, 'history.txt')
                else:
                    if os.path.exists(os.path.join(home, 'History', site, 'history.txt')):
                        file_path = os.path.join(home, 'History', site, 'history.txt')
                row = self.currentRow()
                if row == (self.count() - 1):
                    next_row = 0
                else:
                    next_row = row+1
                ui.original_path_name[row], ui.original_path_name[next_row] = ui.original_path_name[next_row], ui.original_path_name[row]
                if os.path.exists(file_path):
                    write_files(file_path, ui.original_path_name, line_by_line=True)
                self.clear()
                for i in ui.original_path_name:
                    if '	' in i:
                        i = i.split('	')[0]
                    self.addItem(i)
                self.setCurrentRow(next_row)
        elif event.key() == QtCore.Qt.Key_Delete:
            param_dict = ui.get_parameters_value(b='bookmark', s='site')
            bookmark = param_dict['bookmark']
            site= param_dict['site']
            r = self.currentRow()
            item = self.item(r)
            if item:
                if site == "PlayLists" and not bookmark:
                    index = self.currentRow()
                    item_r  = self.item(index)
                    if item_r:
                        item = str(self.currentItem().text())
                        if item != "Default":
                            file_pls = os.path.join(home, 'Playlists', item)
                            if os.path.exists(file_pls):
                                os.remove(file_pls)
                            self.takeItem(index)
                            del item_r
                            ui.list2.clear()
                elif site == "Video" and not bookmark:
                    video_db = os.path.join(home, 'VideoDB', 'Video.db')
                    conn = sqlite3.connect(video_db)
                    cur = conn.cursor()
                    txt = ui.original_path_name[r].split('	')[1]
                    cur.execute('Delete FROM Video Where Directory=?', (txt, ))
                    logger.info('Deleting Directory From Database : '+txt)
                    del ui.original_path_name[r]
                    conn.commit()
                    conn.close()
                    self.takeItem(r)
                    del item
                    if txt in ui.video_dict:
                        del ui.video_dict[txt]
                elif site == "Music" and not bookmark:
                    list3n = (ui.list3.currentItem().text())
                    if (list3n == "Fav-Artist" or list3n == "Fav-Album" 
                            or list3n=="Fav-Directory" or list3n == 'Artist'
                            or list3n == 'Album' or list3n == 'Title'
                            or list3n == 'Directory'):
                        conn = sqlite3.connect(os.path.join(home, 'Music', 'Music.db'))
                        cur = conn.cursor()
                        qVal = ui.original_path_name[r]
                        logger.info('{0}--qval'.format(qVal))
                        qr = None
                        if list3n == "Fav-Artist":
                            qr = 'Update Music Set Favourite="no" Where Artist=?'
                        elif list3n == "Fav-Album":
                            qr = 'Update Music Set Favourite="no" Where Album=?'
                        elif list3n == "Fav-Directory":
                            qr = 'Update Music Set Favourite="no" Where Directory=?'
                        elif list3n == "Artist":
                            qr = 'Delete From Music Where Artist=?'
                        elif list3n == 'Album':
                            qr = 'Delete From Music Where Album=?'
                        elif list3n == "Directory":
                            qr = 'Delete From Music Where Directory=?'
                        if qr:
                            cur.execute(qr, (qVal, ))
                            logger.debug('qr={0}::qVal={1}'.format(qr, qVal))
                            self.takeItem(r)
                            del item
                            logger.info("Number of rows updated: %d" % cur.rowcount)
                            del ui.original_path_name[r]
                        conn.commit()
                        conn.close()
                        self.setCurrentRow(r)
                elif site == 'None':
                    print("Nothing to delete")
                else:
                    ui.deleteHistory()
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_H:
            ui.setPreOpt('fromtitlelist')
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_R:
            ui.shuffleList()
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_T:
            ui.sortList()
        elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Y:
            ui.getList()
        elif event.key() == QtCore.Qt.Key_Return:
            ui.list1_double_clicked()
        elif event.key() == QtCore.Qt.Key_Right:
            ui.list2.setFocus()
        elif event.key() == QtCore.Qt.Key_F2:
            if ui.original_path_name:
                print('F2 Pressed')
                if self.currentItem():
                    self.edit_name_list1(self.currentRow())
        elif event.key() == QtCore.Qt.Key_Left:
            if ui.tab_5.isHidden() and ui.mpvplayer_val.processId() == 0:
                ui.btn1.setFocus()
                ui.dockWidget_3.show()
            else:
                ui.tab_5.setFocus()
        elif event.key() == QtCore.Qt.Key_Period:
            site = ui.get_parameters_value(s='site')['site']
            if site == "Music":
                ui.mpvNextEpnList()
            else:
                ui.nextp(ui.list3.currentRow())
        elif event.key() == QtCore.Qt.Key_Comma:
            site = ui.get_parameters_value(s='site')['site']
            if site == "Music":
                ui.mpvPrevEpnList()
            else:
                ui.backp(ui.list3.currentRow())
        elif event.key() == QtCore.Qt.Key_Down:
            nextr = self.currentRow() + 1
            if nextr == self.count():
                self.setCurrentRow(0)
            else:
                self.setCurrentRow(nextr)
        elif event.key() == QtCore.Qt.Key_Up:
            prev_r = self.currentRow() - 1
            if self.currentRow() == 0:
                self.setCurrentRow(self.count()-1)
            else:
                self.setCurrentRow(prev_r)
        else:
            super(TitleListWidget, self).keyPressEvent(event)
            
    def set_search_backend(self, use_search=None):
        if use_search is None:
            use_search = False
        try:
            site = ui.get_parameters_value(s='site')['site']
            nm = ui.get_title_name(self.currentRow())
            ui.posterfound_new(
                name=nm, site=site, url=False, copy_poster=True, copy_fanart=True, 
                copy_summary=True, direct_url=False, use_search=use_search)
        except Exception as e:
            print(e)
            
    def get_all_information(self):
        backend = ['duckduckgo+tvdb', 'duckduckgo+tmdb', 'google+tvdb', 'google+tmdb']
        backend_dict = {
            'duckduckgo+tvdb':'tvdb+ddg', 'duckduckgo+tmdb':'tmdb+ddg',
            'google+tvdb':'tvdb+g', 'google+tmdb':'tmdb+g'
            }
        item, ok = QtWidgets.QInputDialog.getItem(
            MainWindow, 'Input Dialog', '         Select Search Backend         ',
            backend, 0, False)
        if item and ok:
            logger.info(item)
            try:
                ui.posterfind_batch = 0
                site = ui.get_parameters_value(s='site')['site']
                opt = ''
                if ui.list3.currentItem():
                    opt = ui.list3.currentItem().text().lower()
                nm = ui.get_title_name(0)
                use_search = backend_dict[item]
                logger.info('\nsite={0}::opt={1}::search={2}\n'.format(site, opt, use_search))
                ui.posterfound_new(
                    name=nm, site=site, url=False, copy_poster=True, copy_fanart=True, 
                    copy_summary=True, direct_url=False, use_search=use_search, get_all=True)
            except Exception as e:
                print(e)
                
    def addBookmarkList(self):
        try:
            new_path = ui.original_path_name[self.currentRow()].split('	')[-1]
        except Exception as e:
            print(e)
            new_path = 'NONE'
        param_dict = ui.get_parameters_value(b='bookmark', o='opt')
        bookmark = param_dict['bookmark']
        opt = param_dict['opt']
        if not bookmark:
            if opt != "History":
                ui.listfound()
            param_dict = ui.get_parameters_value(
                s='site', sn='siteName', bu='base_url', e='embed', v='video_local_stream',
                n='name', r='refererNeeded', f='finalUrlFound')
            site = param_dict['site']
            siteName = param_dict['siteName']
            base_url = param_dict['base_url']
            embed = param_dict['embed']
            name = param_dict['name']
            refererNeeded = param_dict['refererNeeded']
            finalUrlFound = param_dict['finalUrlFound']
            video_local_stream = param_dict['video_local_stream']
            if site == "Music" or site == "Video":
                if ui.list3.currentItem():
                    music_opt = str(ui.list3.currentItem().text())
                    tmp = site+':'+(music_opt)+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)+':'+str(video_local_stream)+':'+str(new_path)
                else:
                    return 0
            else:
                tmp = site+':'+"History"+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)+':'+str(video_local_stream)+':'+str(new_path)
            file_path = os.path.join(home, 'Bookmark', 'bookmark.txt')
            write_files(file_path, tmp, line_by_line=True)
            note = name + " is Bookmarked"

    def triggerBookmark(self, val):
        try:
            new_path = ui.original_path_name[self.currentRow()].split('	')[-1]
        except Exception as e:
            print(e)
            new_path = 'NONE'
        param_dict = ui.get_parameters_value(b='bookmark', o='opt')
        bookmark = param_dict['bookmark']
        opt = param_dict['opt']
        if not bookmark:
            self.addBookmarkList()
        param_dict = ui.get_parameters_value(
            s='site', sn='siteName', bu='base_url', e='embed', v='video_local_stream',
            n='name', r='refererNeeded', f='finalUrlFound')
        site = param_dict['site']
        siteName = param_dict['siteName']
        base_url = param_dict['base_url']
        embed = param_dict['embed']
        name = param_dict['name']
        refererNeeded = param_dict['refererNeeded']
        finalUrlFound = param_dict['finalUrlFound']
        video_local_stream = param_dict['video_local_stream']
        if site == "Music" or site == "Video":
            if ui.list3.currentItem():
                music_opt = str(ui.list3.currentItem().text())
                tmp = site+':'+(music_opt)+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)+':'+str(video_local_stream)+':'+str(new_path)
            else:
                return 0
        else:
            if ui.list1.currentItem():
                tmp = site+':'+"History"+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)+':'+str(video_local_stream)+':'+str(new_path)
            else:
                return 0
        file_path = os.path.join(home, 'Bookmark', val+'.txt')
        if os.path.isfile(file_path):
            lines = open_files(file_path, True)
            lines = [i.strip() for i in lines if i.strip()]
            lines.append(tmp)
            write_files(file_path, lines, line_by_line=True)
            note = name + " is Added to "+val+" Category"
            send_notification(note, code=0)

    def triggerPlaylist(self, value):
        print('Menu Clicked')
        print(value)
        file_path = os.path.join(home, 'Playlists', str(value))
        for i in range(len(ui.epn_arr_list)):
            if os.path.exists(file_path):
                sumr=str(ui.epn_arr_list[i].split('	')[0])
                try:
                    rfr_url=str(ui.epn_arr_list[i].split('	')[2])
                except:
                    rfr_url = "NONE"
                sumry = str(ui.epn_arr_list[i].split('	')[1])
                sumry = sumry.replace('"', '')
                sumry = '"'+sumry+'"'
                t = sumr+'	'+sumry+'	'+rfr_url
                write_files(file_path, t, line_by_line=True)
    
    def update_video_category(self, site, txt):
        if site.lower() == 'video' and self.currentItem():
            category = ui.category_dict.get(txt.lower())
            if category:
                rows = [i.split('\t')[1] for i in ui.epn_arr_list]
                conn = sqlite3.connect(os.path.join(home, 'VideoDB', 'Video.db'))
                cur = conn.cursor()
                for i in rows:
                    qr = 'Update Video Set Category=? Where Path=?'
                    cur.execute(qr, (category, i))
                    logger.info('{0}::{1}'.format(category, i))
                conn.commit()
                conn.close()
                msg = '{0} Successfully Added to category: {1}'.format(self.currentItem().text(), txt)
            else:
                msg = 'Invalid Category'
        else:
            msg = 'This operation not allowed in this section'
        send_notification(msg, code=0)
        logger.info('{0}: --588--{1}'.format(msg, ui.category_dict))
        
    def delete_category_video(self, site, category):
        cat_val = ui.category_dict.get(category.lower())
        if cat_val and site.lower() == 'video':
            conn = sqlite3.connect(os.path.join(home, 'VideoDB', 'Video.db'))
            cur = conn.cursor()
            qr = 'Update Video Set Category=? Where Category=?'
            cur.execute(qr, (ui.category_dict['others'], cat_val))
            conn.commit()
            conn.close()
            
            if category in ui.category_array:
                cat_index = ui.category_array.index(category)
                del ui.category_array[cat_index]
            
            del ui.category_dict[category.lower()]
                        
            cat_item = ui.list3.findItems(category, QtCore.Qt.MatchExactly)
            if cat_item:
                list_item = cat_item[0]
                list_item_row = ui.list3.row(list_item)
                ui.list3.takeItem(list_item_row)
                del list_item
            
            cat_file = os.path.join(home, 'VideoDB', 'extra_category')
            if os.path.isfile(cat_file):
                lines = open_files(cat_file, True)
                lines = [i.strip() for i in lines if i.strip()]
                if category in lines:
                    line_index = lines.index(category)
                    del lines[line_index]
                    write_files(cat_file, lines, line_by_line=True)
                    
            logger.info('Category {0} set to ::{1}'.format(category, 'Others'))
            logger.info('Category Dict: {0}\nCategory Array: {1}'.format(ui.category_dict, ui.category_array))
            msg = 'Category {0} Removed; Removed Items are in Others Category'.format(category)
            send_notification(msg, code=0)
        else:
            send_notification('Wrong Parameters')
            
    def edit_name_list1(self, row):
        site = ui.get_parameters_value(s='site')['site']
        if '	' in ui.original_path_name[row]:
            default_text = ui.original_path_name[row].split('	')[0]
            default_path_name = ui.original_path_name[row].split('	')[1]
            default_basename = os.path.basename(default_path_name)
        else:
            default_text = ui.original_path_name[row]
        default_display = 'Enter Title Name Manually\nCurrent Title:\n{0}'.format(default_text)
        item, ok = QtWidgets.QInputDialog.getText(
            MainWindow, 'Input Dialog', default_display, 
            QtWidgets.QLineEdit.Normal, default_text)
        if ok and item:
            nm = item
            #row = self.currentRow()
            old_val = ui.original_path_name[row]
            logger.info("4282:{0}:{1}:{2}".format(nm, row, old_val))
            if site == "Video":
                itemlist = ui.list1.item(row)
                if itemlist:
                    if itemlist.text() == item:
                        msg = 'name already exists'
                        send_notification(msg)
                    else:
                        home_dir_new = os.path.join(home, 'Local', item)
                        video_db = os.path.join(home, 'VideoDB', 'Video.db')
                        conn = sqlite3.connect(video_db)
                        cur = conn.cursor()
                        old_name, directory = old_val.split('\t')
                        qr = 'Update Video Set Title=? Where Directory=?'
                        logger.info('{0}::{1}'.format(nm, directory))
                        cur.execute(qr, (nm, directory))
                        conn.commit()
                        conn.close()
                        tmp = re.sub('[^	]*', item, old_val, 1)
                        ui.original_path_name[row] = tmp
                        itemlist.setText(item)
                        home_dir_old = os.path.join(home, 'Local', old_name)
                        if os.path.exists(home_dir_old):
                            if os.path.exists(home_dir_new):
                                shutil.rmtree(home_dir_old)
                                msg = '\nFolder: {0} already exists thus removing {1}\n'.format(home_dir_new, home_dir_old)
                                logger.info(msg)
                            else:
                                shutil.move(home_dir_old, home_dir_new)
                                logger.info('\nmoving {0}::to::{1}\n'.format(home_dir_old, home_dir_new))
            elif site.lower() == 'playlists':
                new_pls_name = os.path.join(home, 'Playlists', item)
                if not os.path.isfile(new_pls_name):
                    itemlist = ui.list1.item(row)
                    if itemlist:
                        old_pls_name = os.path.join(home, 'Playlists', itemlist.text())
                        if os.path.isfile(old_pls_name) and not os.path.isfile(new_pls_name):
                            shutil.move(old_pls_name, new_pls_name)
                            itemlist.setText(item)
                else:
                    msg = 'file already exists'
                    send_notification(msg)
            elif site.lower() == 'music' or site.lower() == 'none':
                pass
            else:
                itemlist = ui.list1.item(row)
                if  itemlist:
                    siteName = ui.get_parameters_value(s='siteName')['siteName']
                    item_value = ui.original_path_name[row]
                    if '\t' in item_value:
                        old_name = item_value.split('\t')[0]
                    else:
                        old_name = item_value
                    if site.lower() == 'subbedanime' or site.lower() == 'dubbedanime':
                        history_txt = os.path.join(home, 'History', site, siteName, 'history.txt')
                        file_dir_new = os.path.join(home, 'History', site, siteName, item)
                        file_dir_old = os.path.join(home, 'History', site, siteName, old_name)
                    else:
                        history_txt = os.path.join(home, 'History', site, 'history.txt')
                        file_dir_new = os.path.join(home, 'History', site, item)
                        file_dir_old = os.path.join(home, 'History', site, old_name)
                    tmp = re.sub('[^	]*', item, item_value, 1)
                    ui.original_path_name[row] = tmp
                    write_files(history_txt, ui.original_path_name, line_by_line=True)
                    itemlist.setText(item)
                    if os.path.exists(file_dir_old):
                        if not os.path.exists(file_dir_new):
                            shutil.move(file_dir_old, file_dir_new)
                            logger.info('\nmoving {0}::to::{1}\n'.format(file_dir_old, file_dir_new))
                        else:
                            shutil.rmtree(file_dir_old)
                            msg = '\nFolder: {0} already exists thus removing {1}\n'.format(file_dir_new, file_dir_old)
                            logger.info(msg)
                    
    def contextMenuEvent(self, event):
        if self.currentItem():
            name = str(ui.list1.currentItem().text())
        else:
            name = ''
        ui.set_parameters_value(name_val=name)
        site = ui.get_parameters_value(s='site')['site']
        if site == "Music":
            menu = QtWidgets.QMenu(self)
            submenuR = QtWidgets.QMenu(menu)
            submenuR.setTitle("Add To PlayList")
            menu.addMenu(submenuR)
            fav = menu.addAction("Add To Favourite")
            r = ui.list3.currentRow()
            itm = ui.list3.item(r)
            if itm:
                music_opt = str(itm.text())
            else:
                music_opt = ""
            pls = os.listdir(os.path.join(home, 'Playlists'))
            item_m = []
            for i in pls:
                i = i.replace('.txt', '')
                item_m.append(submenuR.addAction(i))
            submenuR.addSeparator()
            new_pls = submenuR.addAction("Create New Playlist")
            profile = menu.addAction("Find Last.fm Profile(manually)")
            default = menu.addAction("Set Default Background")
            delPosters = menu.addAction("Delete Poster")
            delFanart = menu.addAction("Delete Fanart")
            delThumb = menu.addAction("Delete Playlist Thumbnails")
            delInfo = menu.addAction("Delete Info")
            thumbnail = menu.addAction("Show Thumbnail View (Ctrl+Z)")
            cache = menu.addAction("Clear Cache")
            action = menu.exec_(self.mapToGlobal(event.pos()))

            for i in range(len(item_m)):
                if action == item_m[i]:
                    self.triggerPlaylist(pls[i].replace('.txt', ''))

            if action == fav:
                r = self.currentRow()
                item = self.item(r)
                if (item and music_opt!="Playlist" 
                        and music_opt!= "Fav-Artist" 
                        and music_opt!= "Fav-Album" 
                        and music_opt!= "Fav-Directory"):
                    txt = str(item.text())
                    ui.media_data.update_music_count('fav', txt)
                else:
                    print("Not Permitted")
            elif action == cache:
                    m = os.listdir(TMPDIR)
                    for i in m:
                        if '.txt' in i or '.jpg' in i:
                            t = os.path.join(TMPDIR, i)
                            os.remove(t)
            elif action == new_pls:
                print("creating")
                item, ok = QtWidgets.QInputDialog.getText(
                    MainWindow, 'Input Dialog', 'Enter Playlist Name')
                if ok and item:
                    file_path = os.path.join(home, 'Playlists', item)
                    if not os.path.exists(file_path):
                        f = open(file_path, 'w')
                        f.close()
            elif action == profile:
                if '/' in name:
                    nam = name.replace('/', '-')
                else:
                    nam = name
                ui.reviewsWeb(srch_txt=nam, review_site='last.fm', 
                              action='search_by_name')
            elif action == thumbnail:
                param_dict = ui.get_parameters_value(b='bookmark', o='opt')
                opt = param_dict['opt']
                bookmark = param_dict['bookmark']
                if (site == "Local" or bookmark 
                        or opt == "History" or site == "Video" 
                        or site == "Music"):
                    if ui.list3.currentItem():
                        if (ui.list3.currentItem().text())=="Artist":
                            ui.scrollArea.setFocus()
                            ui.lock_process = True
                            ui.IconView()
                            ui.lock_process = False
            elif (action == delInfo or action == delPosters 
                    or action == default or action == delThumb 
                    or action == delFanart):
                if (ui.list3.currentItem()):
                    if str(ui.list3.currentItem().text()) == "Artist":
                        if '/' in name:
                            nam = name.replace('/', '-')
                        else:
                            nam = name
                    else:
                        try:
                            r = ui.list2.currentRow()
                            nam = ui.epn_arr_list[r].split('	')[2]
                        except:
                            nam = ""
                        if '/' in nam:
                            nam = nam.replace('/', '-')
                        else:
                            nam = nam
                    if nam:
                        picn = os.path.join(home, 'Music', 'Artist', nam, 
                                            'poster.jpg')
                        fanart = os.path.join(home, 'Music', 'Artist', nam, 
                                              'fanart.jpg')
                        default_wall = os.path.join(home, 'default.jpg')
                        sumr = os.path.join(home, 'Music', 'Artist', nam, 
                                            'bio.txt')
                        dir_n = os.path.join(home, 'Music', 'Artist', nam)
                        if os.path.exists(dir_n):
                            if action == delInfo:
                                m = os.listdir(dir_n)
                                for i in m:
                                    if i.endswith('.txt'):
                                        f = open(os.path.join(dir_n, 'bio.txt'), 'w')
                                        f.write('No Information Available')
                                        f.close()
                                m = os.listdir(TMPDIR)
                                for i in m:
                                    if i.endswith('.jpg') or i.endswith('.txt'):
                                        t = os.path.join(TMPDIR, i)
                                        os.remove(t)
                            elif action == delPosters:
                                m = os.listdir(dir_n)
                                for i in m:
                                    if i.endswith('.jpg'):
                                        os.remove(os.path.join(dir_n, i))
                                m = os.listdir(TMPDIR)
                                for i in m:
                                    if i.endswith('.jpg') or i.endswith('.txt'):
                                        t = os.path.join(TMPDIR, i)
                                        os.remove(t) 
                            elif action == delThumb:
                                m = os.listdir(dir_n)
                                for i in m:
                                    logger.info(i)
                                    if i.startswith('256px') or i.startswith('128px'):
                                        os.remove(os.path.join(dir_n, i))
                                m = os.listdir(TMPDIR)
                                for i in m:
                                    if i.startswith('256x') or i.startswith('128x'):
                                        t = os.path.join(TMPDIR, i)
                                        os.remove(t) 
                            elif action == delFanart:
                                m = os.listdir(dir_n)
                                for i in m:
                                    if (i.startswith('fanart') or i.startswith('original-fanart')):
                                        os.remove(os.path.join(dir_n, i))
                                m = os.listdir(TMPDIR)
                                for i in m:
                                    if i.startswith('fanart') or i.startswith('original-fanart'):
                                        t = os.path.join(TMPDIR, i)
                                        os.remove(t)
                            elif action == default:
                                shutil.copy(default_wall, picn)
                                shutil.copy(default_wall, fanart)
                                ui.videoImage(
                                    picn, os.path.join(home, 'Music', 'Artist',
                                    nam, 'thumbnail.jpg'), fanart, '')
        else:
            menu = QtWidgets.QMenu(self)
            submenuR = QtWidgets.QMenu(menu)
            submenuR.setTitle("Find Information")
            menu.addMenu(submenuR)
            
            menu_cat = QtWidgets.QMenu(menu)
            menu_cat.setTitle("Add To Category")
            if site.lower() == 'video':
                menu.addMenu(menu_cat)
                
            submenu = QtWidgets.QMenu(menu)
            submenu.setTitle("Bookmark Options")
            menu.addMenu(submenu)
            
            menu_search = QtWidgets.QMenu(menu)
            menu_search.setTitle('Poster Options')
            menu.addMenu(menu_search)
            
            if 'AnimeWatch' in home or ui.anime_review_site:
                submenu_arr_dict = {
                    'mal':'MyAnimeList', 'ap':'Anime-Planet', 
                    'ans':'Anime-Source', 'tvdb':'TVDB', 'tmdb':'TMDB',
                    'ann':'ANN', 'anidb':'AniDB', 'g':'Google', 
                    'yt':'Youtube', 'ddg':'DuckDuckGo', 
                    'last.fm':'last.fm', 'zerochan':'Zerochan'
                    }
            elif 'kawaii-player' in home:
                submenu_arr_dict = {
                    'tvdb':'TVDB', 'tmdb':'TMDB', 'g':'Google', 
                    'yt':'Youtube', 'ddg':'DuckDuckGo', 
                    'last.fm':'last.fm'
                    }
            reviews = []
            for i in submenu_arr_dict:
                reviews.append(submenuR.addAction(submenu_arr_dict[i]))
            addBookmark = submenu.addAction("Add Bookmark")
            bookmark_array = ['bookmark']
            book_dir = os.path.join(home, 'Bookmark')
            pls = os.listdir(book_dir)
            
            pls = sorted(
                pls, key=lambda x: os.path.getmtime(os.path.join(book_dir, x)),
                reverse=True)
            item_m = []
            for i in pls:
                i = i.replace('.txt', '')
                logger.info(i)
                if i not in bookmark_array:
                    item_m.append(submenu.addAction(i))
            submenu.addSeparator()
            new_pls = submenu.addAction("Create New Bookmark Category")
            history = menu.addAction("History (Ctrl+H)")
            thumbnail = menu.addAction("Thumbnail View (Ctrl+Z)")
            cat_arr = []
            for i in ui.category_array:
                cat_arr.append(menu_cat.addAction(i))
            menu_cat.addSeparator()
            add_cat = menu_cat.addAction('Create Category')
            del_cat = menu_cat.addAction('Delete Category')
            
            tvdb = menu_search.addAction("Find Poster(TVDB) (Alt+1)")
            tmdb = menu_search.addAction("Find Poster(TMDB) (Alt+2)")
            menu_search.addSeparator()
            ddg_tvdb = menu_search.addAction("Find Poster(ddg+tvdb) (Ctrl+Right)")
            ddg_tmdb = menu_search.addAction("Find Poster(ddg+tmdb) (Ctrl+Left)")
            glinks_tvdb = menu_search.addAction("Find Poster(g+tvdb) (Ctrl+Up)")
            glinks_tmdb = menu_search.addAction("Find Poster(g+tmdb) (Ctrl+Down)")
            menu_search.addSeparator()
            poster_all = menu_search.addAction("Find Posters for All (Ctrl+A)")
            
            menu_clear = QtWidgets.QMenu(menu)
            menu_clear.setTitle('Clear')
            menu.addMenu(menu_clear)
            
            cache = menu_clear.addAction("Clear Cache")
            del_history = menu_clear.addAction("Delete (History or Bookmark Item)")
            rem_fanart = menu_clear.addAction("Remove Fanart")
            rem_poster = menu_clear.addAction("Remove poster")
            refresh_poster = menu_clear.addAction("Refresh posters")
            rename = menu.addAction("Rename (F2)")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            
            if action in item_m:
                item_index = item_m.index(action)
                self.triggerBookmark(item_m[item_index].text())
            elif action in reviews:
                item_index = reviews.index(action)
                new_review = reviews[item_index].text()
                if new_review.startswith('&'):
                    new_review = new_review[1:]
                st = 'ddg'
                for i in submenu_arr_dict:
                    if submenu_arr_dict[i].lower() == new_review.lower():
                        st = i
                        break
                ui.reviewsWeb(srch_txt=name, review_site=st, action='context_menu')
            elif action == new_pls:
                print("creating new bookmark category")
                item, ok = QtWidgets.QInputDialog.getText(
                    MainWindow, 'Input Dialog', 'Enter Playlist Name')
                if ok and item:
                    file_path = os.path.join(home, 'Bookmark', item+'.txt')
                    if not os.path.exists(file_path):
                        f = open(file_path, 'w')
                        f.close()
            elif action == del_history:
                ui.deleteHistory()
            elif action in cat_arr:
                txt = action.text()
                self.update_video_category(site, txt)
            elif action == add_cat:
                item, ok = QtWidgets.QInputDialog.getText(
                    MainWindow, 'Input Dialog', 'Add New Category to Video', 
                    QtWidgets.QLineEdit.Normal, 'Edit')
                if item and ok:
                    cat_path = os.path.join(home, 'VideoDB', 'extra_category')
                    if not os.path.isfile(cat_path):
                        open(cat_path, 'w').close()
                    if item.lower() not in ui.category_dict:
                        lines = open_files(cat_path, True)
                        lines = [i.strip() for i in lines if i.strip()]
                        lines.append(item)
                        write_files(cat_path, lines, line_by_line=True)
                        ui.category_array.append(item)
                        ui.category_dict.update({item.lower():item})
                        row = ui.list3.findItems('Update',QtCore.Qt.MatchExactly)
                        ui.list3.insertItem(ui.list3.row(row[0]), item)
                    else:
                        send_notification('Category Already Exists')
            elif action == del_cat:
                cat_list = [ui.category_array[i] for i in range(5, len(ui.category_array))]
                if cat_list:
                    item, ok = QtWidgets.QInputDialog.getItem(
                        MainWindow, 'Input Dialog', 'Select Extra Category To Remove from Video Section',
                        cat_list, 0, False)
                    if item and ok:
                        self.delete_category_video(site, item)
            elif action == addBookmark:
                self.addBookmarkList()
            elif action == thumbnail:
                param_dict = ui.get_parameters_value(b='bookmark', o='opt',
                                                     s='site')
                opt = param_dict['opt']
                bookmark = param_dict['bookmark']
                site = param_dict['site']
                if ((site == "Local" or site == 'PlayLists') 
                        or bookmark or opt == "History" 
                        or site == "Video"):
                    ui.scrollArea.setFocus()
                    ui.lock_process = True
                    ui.IconView()
                    ui.lock_process = False
            elif action == cache:
                m = os.listdir(TMPDIR)
                for i in m:
                    file_name = os.path.join(TMPDIR, i)
                    if os.path.isfile(file_name):
                        os.remove(file_name)
                    if os.path.isdir(file_name):
                        shutil.rmtree(file_name)
            elif action == tvdb:
                self.set_search_backend(use_search=False)
            elif action == tmdb:
                self.set_search_backend(use_search='tmdb')
            elif action == glinks_tvdb:
                self.set_search_backend(use_search='tvdb+g')
            elif action == glinks_tmdb:
                self.set_search_backend(use_search='tmdb+g')
            elif action == ddg_tvdb:
                self.set_search_backend(use_search=True)
            elif action == ddg_tmdb:
                self.set_search_backend(use_search='tmdb+ddg')
            elif action == poster_all:
                self.get_all_information()
            elif action == rename:
                if ui.original_path_name:
                    print('Renaming')
                    if self.currentItem():
                        self.edit_name_list1(self.currentRow())
            elif action == history:
                ui.setPreOpt('fromtitlelist')
            elif action == rem_fanart:
                path = ui.get_current_directory()
                fanart = os.path.join(path, 'fanart.jpg')
                fanart_original = os.path.join(path, 'original-fanart.jpg')
                if os.path.exists(fanart):
                    os.remove(fanart)
                if os.path.exists(fanart_original):
                    os.remove(fanart_original)
            elif action == rem_poster:
                path = ui.get_current_directory()
                fanart = os.path.join(path, 'poster.jpg')
                fanart_original = os.path.join(path, 'thumbnail.jpg')
                if os.path.exists(fanart):
                    os.remove(fanart)
                if os.path.exists(fanart_original):
                    os.remove(fanart_original)
            elif action == refresh_poster:
                path = ui.get_current_directory()
                fanart_original = os.path.join(path, 'thumbnail.jpg')
                if os.path.exists(fanart_original):
                    os.remove(fanart_original)
