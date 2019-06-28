import queue
import messages
import threading


class Start(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.running = True
        self.main_list = []
        self.firstCall = True
        self.ingestText()

    def run(self):
        while self.running:
            task = self.queue.get()
            if task is None:
                break
            task.run(self)
            self.queue.task_done()

    def PostMessage(self, message):
        self.queue.put(message)


    # Replace Category:
    # ------------------------------------------
    # num_cat: The category number to be replaced
    # c_list: The list new list of Category, Questions and Answers
    # This function simply replaces the current list of Categories, Questions, and Answers
    #	and writes the new main_list to the original text file in its original format  
    #   should be called whenever the user has saved a change to the questions/answers

    def replaceCategory(self, num_cat, c_list):
        if num_cat < 5:
            self.main_list[num_cat] = c_list
        else:
            pass
        textfile = "resource/category_question_answer.txt"
        f = open(textfile, "w")
        for list in self.main_list:
            for item in list:
                outstring=item+"\n"
                f.write(outstring)
        f.close()

    # Ingest Text:
    # ------------------------------------------
    # This function reads from the category_question_answer.txt file that is storing the 
    #    current Categories, questions, and answers. While it is reading the file, it is 
    #    sorting each category with its questions and answers into its own list, and then
    #    appending that to its master list. Should be called during the init of the class
    #    Text file format is as follows:
    #	 	Category: <Name of Category 1>
    #		<Question 1 of Category 1>
    #		<Answer 1 of Category 1>
    #		. . .
    #		<Answer 6 of Category 1>
    # 		Category: <Name of Category 2>
    # 		. . .

    def ingestText(self):
        temp_list = []
        textfile = "resource/category_question_answer.txt"
        f = open(textfile, "r")
        for line in f.readlines():
            if "Category:" in line:
                category = line.split("Category: ")
                if self.firstCall:
                    temp_list.append(category[len(category)-1].strip())
                    self.firstCall = False
                else:
                    self.main_list.append(temp_list)
                    temp_list = []
                    temp_list.append(category[len(category)-1].strip())
                self.firstCall = False
            else:
                temp_list.append(line.strip())
        f.close()
