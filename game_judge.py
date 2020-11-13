import datetime
import threading

class PendingGame:
    def __init__(self, main_field, text, type):
        # основное поле
        self.field = main_field
        # текст
        self.text = text
        # words separated
        self.text_word = text.split()
        # index of cur word
        self.cur_word_ind = 0
        # cur word
        self.cur_word_let = self.text_word[0] + ' '
        # flag for first letter
        self.first_letter = True
        # connect line edit with our programm
        self.field.tr_writing_area.textChanged.connect(self.check_position)
        # errors counter
        self.errors = 0
        # index of current letter in the texst
        self.ind = 0
        # connect threads with info item
        self.reload_speed()
        # index for result
        self.error_ind = []
        # if user write a wrong letter other are not available
        self.onError = False
        self.exc = 1
        self.last_ind = 0
        self.last_success = 0
        # print(self.text, self.ind)
        self.type = type
        self.value = 'border: 5px solid #aa0000;'
        self.memory = {}
        self.field.tr_writing_area.setFocus()
        # creating layout
        if self.field.cur_language == self.field.RUSSIAN:
            self.layout = self.field.RUSSIAN_LAYOUT
        else:
            self.layout = self.field.ENGLISH_LAYOUT
        # contuting first letter-button
        for item in self.layout[self.text[0]]:
            self.memory[item] = item.styleSheet()
            item.setStyleSheet(self.memory[item] + self.value)

    def check_position(self):
        ''' check letters in current word
        calling if LineEdit text had changed'''
        try:
            for key, value in self.memory.items():
                key.setStyleSheet(value)
            # if nothing to type return None
            if len(self.text_word) == 0:
                return None
            # reading value in lineEdit
            cur_value = self.field.tr_writing_area.text()

            # if first letter is done we can move on
            if self.first_letter:
                
                self.first_letter = False

                self.begin_time = datetime.datetime.now()

                self.field.tr_first_letter.hide()
            
            # if cur_value is longer than current word returned None
            if len(cur_value) > len(self.cur_word_let):
                return None
            
            if len(cur_value) != 0:
                # checking our letters if is correct 
                # generate our new text and values
                if self.cur_word_let[len(cur_value) - 1] == cur_value[-1] and self.last_success + 1 >= len(cur_value):

                    self.onError = False

                    self.ind = self.last_ind + len(cur_value)
                    if self.ind < len(self.text):
                        for item in self.layout[self.text[self.ind]]:
                            self.memory[item] = item.styleSheet()
                            item.setStyleSheet(self.memory[item] + self.value)

                    # if letter are later than last typed word is wrong letter
                    # so, let's storage last success letter
                    self.last_success = len(cur_value)

                    self.cur_word_ind = len(cur_value) - 1

                    # remaking text with colors

                    self.field.tr_text_field.setText(f"<font color=\"#ffaa00\">" + 
                                f"{self.text[:self.ind]}</font>{self.text[self.ind:]}")

                    # making new word if in this letters are other
                    if (len(self.cur_word_let) == len(cur_value)):
                        # ending game
                        if len(self.text_word) == 0:
                            self.word = "^&*()"
                            self.end_of_game()
                            return None

                        # remove elemnt from index
                        self.text_word.remove(self.text_word[0])

                        if len(self.text_word):
                            self.cur_word_let = self.text_word[0]
                        else:
                            self.word = "^&*()"
                            self.end_of_game()
                            return None
                        if len(self.text_word) > 1:
                            self.cur_word_let += ' '

                        # change buffer to restore our buttons start possition
                        for key, value in self.memory.items():
                            key.setStyleSheet(value)

                        self.cur_word_ind = 0
                        self.field.tr_writing_area.setText("")
                        self.last_ind = self.ind
                        # set our current possition
                        for item in self.layout[self.text[self.ind]]:
                            self.memory[item] = item.styleSheet()
                            item.setStyleSheet(self.memory[item] + self.value)
                else:
                    # return button static values
                    for item in self.layout['err']:
                        self.memory[item] = item.styleSheet()
                        item.setStyleSheet(self.memory[item] + self.value)
                    if not self.onError:
                        
                        self.error_ind.append(self.ind)
                        self.errors += 1
                        self.onError = True
                        # playing mp3
                        if self.errors % 5 != 0:
                            self.field.load_mp3('uploads/short_chop.mp3')
                            self.field.player.play()
                        else:
                            self.field.load_mp3('uploads/super_angry.mp3')
                            self.field.player.play()
                        
        except Exception as e:
            print(e)
        

    def reload_speed(self):
        # print(self.errors)
        if self.first_letter:
            threading.Timer(2, self.reload_speed).start() 
            return None
        try:
            # making a esception to kill a thread
            exc = 1 / self.exc
            # counting second
            threading.Timer(2, self.reload_speed).start() 
            seconds = (datetime.datetime.now() - self.begin_time).total_seconds()
            value = int((self.ind + 1) * 60 / seconds)
            self.field.tr_info_panel.setText(f'                                                         Ошибки: {self.errors}'
                                            + f'                                                     Скорость: {value}')
        except Exception as e:
            return None
            
    def ending_without_result(self):
        ''' hide everything that was doing by our programm '''
        for key, value in self.memory.items():
            key.setStyleSheet(value)
        self.exc = 0
        self.field.hide_elements(self.field.tr_area)
        self.field.show_elements(self.field.choose_area)
        self.field.hide_elements(self.field.rez_area)
        self.field.tr_writing_area.setText("")
        self.field.tr_info_panel.setText(f'                                                         Ошибки: 0'
                                        + f'                                                     Скорость: 0')
    
    def end_of_game(self):
        ''' show ending panel and remove the past actions'''
        # return normal values in our buttons
        for key, value in self.memory.items():
            key.setStyleSheet(value)
        
        rez_string = ''
        # set red-mistaken color and green-right color
        for i in range(len(self.text)):
            if i in self.error_ind:
                rez_string += f"<font color=\"#ff0000\">{self.text[i]}</font>"
            else:
                rez_string += f"<font color=\"#00aa00\">{self.text[i]}</font>"
        self.exc = 0
        # creatin speed
        seconds = (datetime.datetime.now() - self.begin_time).total_seconds()
        value = int((self.ind + 1) * 60 // seconds)
        # insert speed
        self.field.tr_info_panel.setText(f'                                                         Ошибки: 0'
                                        + f'                                                     Скорость: 0')
        self.field.rez_mistakes.setText(f'                                                         Ошибки: {self.errors}'
                                            + f'                                                     Скорость: {value}')

        # updating json file
        cur = self.field.json.get_data()
        cur[self.type]['sum'] += value
        cur[self.type]['max_speed'] = max(cur[self.type]['max_speed'], value)
        cur[self.type]['counter'] += 1
        cur[self.type]['avg_value'] = cur[self.type]['sum'] // cur[self.type]['counter']
        self.field.json.set_data(cur)
        self.field.json.write_data()
        self.field.chart_view.hide()
        self.field.create_piechart()
        self.field.reset_table()
        # put right widget possition
        self.field.rez_main_text.setText(rez_string)
        self.field.hide_elements(self.field.tr_area)
        self.field.hide_elements(self.field.choose_area)
        self.field.show_elements(self.field.rez_area)
        self.field.tr_writing_area.setText("")
                