from tkinter import *
from tkinter.filedialog import askopenfilename


# STEP 1: CREATE CANVAS FOR CATEGORY BUTTONS AND LABELS
root = Tk()
root.title("Wheel of Jeopardy: Question/Answer Editor")
root.resizable(width = False, height = False)


final_list = [''] * 2 * 66
start_x = 20
start_y = 50
spacer = 30
rec_len = 150
rec_width = 80
center_x = (start_x + rec_len)/2
center_y = (start_y + rec_width)/2


canvas = Canvas(width= 6 * (rec_len - spacer) + 2 * start_x, height= 15 * (rec_width - spacer) + 2 * start_y)

canvas.pack()


round_label = Label(root, text = 'Round 1', font = 'Helvetica 20 bold')
round_label.place(x = rec_len/2 + start_x/2 + 5, y = spacer, anchor=CENTER)
canvas.create_line(start_x, spacer, rec_len + start_x/2, spacer)
canvas.create_line(start_x/2, 6 * (rec_width - spacer) + 2 * start_y,
                   6 * (rec_len - spacer) + 2 * start_x, 6 * (rec_width - spacer) + 2 * start_y, dash=(4, 2))

round2_label = Label(root, text = 'Round 2', font = 'Helvetica 20 bold')
round2_label.place(x = rec_len/2 + start_x/2 + 5, y = 6* rec_width - 1.5*spacer, anchor=CENTER)
canvas.create_line(start_x, 6* rec_width - 1.5*spacer, rec_len + start_x/2, 6* rec_width - 1.5*spacer)



cat1 = canvas.create_rectangle(start_x,
                               start_y,
                               rec_len,
                               rec_width,
                               fill = "yellow", tags = "cat1a")

cat1_lab = canvas.create_text(center_x,
                              center_y,
                              text="Category 1",
                              font='Helvetica 14 bold', tags = "cat1a")

##########

cat2 = canvas.create_rectangle(start_x,
                               start_y + rec_width - spacer,
                               rec_len,
                               2 * rec_width - spacer,
                               fill = "red", tags = "cat2a")

cat2_lab = canvas.create_text(center_x,
                              center_y + rec_width - spacer,
                              text="Category 2",
                              font='Helvetica 14 bold', tags = "cat2a")

##########

cat3 = canvas.create_rectangle(start_x,
                               start_y + 2 * rec_width - 2 * spacer,
                               rec_len,
                               3 * rec_width - 2 * spacer,
                               fill = "blue", tags = "cat3a")

cat3_lab = canvas.create_text(center_x,
                              center_y + 2 * rec_width - 2 * spacer,
                              text="Category 3",
                              font='Helvetica 14 bold', tags = "cat3a")

##########

cat4 = canvas.create_rectangle(start_x ,
                               start_y + 3 * rec_width - 3 * spacer,
                               rec_len,
                               4 * rec_width - 3 * spacer,
                               fill = "green", tags = "cat4a")

cat4_lab = canvas.create_text(center_x,
                              center_y + 3 * rec_width - 3 * spacer,
                              text="Category 4",
                              font='Helvetica 14 bold', tags = "cat4a")

##########

cat5 = canvas.create_rectangle(start_x,
                               start_y + 4 * rec_width - 4 * spacer,
                               rec_len,
                               5 * rec_width - 4 * spacer,
                               fill = "purple", tags = "cat5a")

cat5_lab = canvas.create_text(center_x,
                              center_y + 4 * rec_width - 4 * spacer,
                              text="Category 5",
                              font='Helvetica 14 bold', tags = "cat5a")

##########

cat6 = canvas.create_rectangle(start_x,
                               start_y + 5 * rec_width - 5 * spacer,
                               rec_len,
                               6 * rec_width - 5 * spacer,
                               fill = "orange", tags = "cat6a")

cat6_lab = canvas.create_text(center_x,
                              center_y + 5 * rec_width - 5 * spacer,
                              text="Category 6",
                              font='Helvetica 14 bold', tags = "cat6a")




cat1r2 = canvas.create_rectangle(start_x,
                               start_y + 8 * rec_width - 8 * spacer + 5,
                               rec_len,
                                 9 * rec_width - 8 * spacer + 5,
                               fill = "yellow", tags = "cat1b")

cat1r2_lab = canvas.create_text(center_x,
                              center_y + 8 * rec_width - 8 * spacer +5,
                              text="Category 1",
                              font='Helvetica 14 bold', tags = "cat1b")

cat2r2 = canvas.create_rectangle(start_x,
                               start_y + 9 * rec_width - 9 * spacer + 5,
                               rec_len,
                                 10 * rec_width - 9 * spacer + 5,
                               fill = "red", tags = "cat1b")

cat2r2_lab = canvas.create_text(center_x,
                              center_y + 9 * rec_width - 9 * spacer +5,
                              text="Category 2",
                              font='Helvetica 14 bold', tags = "cat2b")

cat3r2 = canvas.create_rectangle(start_x,
                               start_y + 10 * rec_width - 10 * spacer + 5,
                               rec_len,
                                 11 * rec_width - 10 * spacer + 5,
                               fill = "blue", tags = "cat3b")

cat3r2_lab = canvas.create_text(center_x,
                              center_y + 10 * rec_width - 10 * spacer +5,
                              text="Category 3",
                              font='Helvetica 14 bold', tags = "cat3b")

cat4r2 = canvas.create_rectangle(start_x,
                               start_y + 11 * rec_width - 11 * spacer + 5,
                               rec_len,
                                 12 * rec_width - 11 * spacer + 5,
                               fill = "green", tags = "cat4b")

cat4r2_lab = canvas.create_text(center_x,
                              center_y + 11 * rec_width - 11 * spacer +5,
                              text="Category 4",
                              font='Helvetica 14 bold', tags = "cat4b")

cat5r2 = canvas.create_rectangle(start_x,
                               start_y + 12 * rec_width - 12 * spacer + 5,
                               rec_len,
                                 13 * rec_width - 12 * spacer + 5,
                               fill = "purple", tags = "cat5b")

cat5r2_lab = canvas.create_text(center_x,
                              center_y + 12 * rec_width - 12 * spacer +5,
                              text="Category 5",
                              font='Helvetica 14 bold', tags = "cat5b")

cat6r2 = canvas.create_rectangle(start_x,
                               start_y + 13 * rec_width - 13 * spacer + 5,
                               rec_len,
                                 14 * rec_width - 13 * spacer + 5,
                               fill = "orange", tags = "cat6b")

cat6r2_lab = canvas.create_text(center_x,
                              center_y + 13 * rec_width - 13 * spacer +5,
                              text="Category 6",
                              font='Helvetica 14 bold', tags = "cat6b")


# CREATE BUTTON TO UPDATE DATA ON SCREEN
saveButton = Button(root, height = 1, width = 15, text = "Update Changes",  command = lambda:[retrieve_input(), show_save_label()])
saveButton.place(x = rec_len + 3 * spacer, y = 14 * (rec_width - spacer) + start_y, anchor = CENTER)

# CREATE BUTTON TO SAVE DATA AND EXIT
saveAndChangeButton = Button(root, height = 1, width = 20, text = "Save Changes and Exit ",  command = lambda:[save_and_quit()])
saveAndChangeButton.place(x = 2*rec_len + 5.25 * spacer, y = 14 * (rec_width - spacer) + start_y, anchor = CENTER)

# CREATE BUTTON TO EXIT WITHOUT SAVING
exitButton = Button(root, height = 1, width = 15, text = "Exit Without Saving",  command = lambda:exit_editor())
exitButton.place(x = 3*rec_len + 6.7 * spacer, y = 14 * (rec_width - spacer) + start_y, anchor = CENTER)

# CREATE BUTTON TO IMPORT FILE
importButton = Button(root, height = 1, width = 15, text = "Import Existing File",
                      command = lambda:select_file())
importButton.place(relx = 0.115, y = 15 * (rec_width - spacer) + start_x + 10, anchor = CENTER)

# CREATE BUTTON TO RESTORE DEFAULT STATE
defaultButton = Button(root, height = 1, width = 15, text = "Restore Default",
                      command = lambda:restore_default())
defaultButton.place(relx = 0.115, y = 15 * (rec_width - spacer) + start_y + 10, anchor = CENTER)

# CREATE BUTTON TO LOAD QUESTIONS LAST USED
loadLastUsedButton = Button(root, height = 1, width = 25, text = "Restore Last Used Questions",
                      command = lambda:load_last_used())
loadLastUsedButton.place(relx = 0.8, y = 15 * (rec_width - spacer) + start_y + 10, anchor = CENTER)

"resources/category_question_answer.txt"



# ADD LABEL FOR THE TITLES
t = Text(root)
t.configure(font = 'Helvetica 14')
t.tag_configure("right", justify='right')
t.tag_add("right", "1.0", "end")
t2 = Text(root)
t2.configure(font = 'Helvetica 14')
t2.tag_configure("right", justify='right')
t2.tag_add("right", "1.0", "end")
l = Label(root, text = 'Select a Category to Edit', font = 'Helvetica 20 bold')
l.place(relx=0.5, y = spacer, anchor=CENTER)
#l2 = Label(root, text = 'Select a Category to Edit', font = 'Helvetica 20 bold')
#l2.place(relx=0.5, y = 6* rec_width - 1.5*spacer,  anchor=CENTER)

# CREATE LABEL FOR WHEN SAVE BUTTON IS PRESSED PRIOR TO SELECTING A CATEGORY
save_label2 = Label(root, text='Please Select a Category to Edit.', font='Helvetica 14 bold')

usage_label = Label(root, text='Each new category must start with "Category". '
                               '\nEach category, question and answer must be on their own separate lines.', font='Helvetica 12 bold')

usage_label.place(relx=0.5, rely = 0.44, anchor=CENTER)




# FUNCTION 1: LOAD THE DATA INTO THE EDITOR
def load_data(filename):

    global filename2
    filename2 = filename

    file = open(filename)

    full_list = list()
    sub_list = list()

    num_cat_lines = 11

    for line in file:
        line = line.rstrip()

        if line.startswith("Category") and len(sub_list) == 0:
             sub_list.append(line)

        if not line.startswith("Category"):
             sub_list.append(line)

        if len(sub_list) == num_cat_lines:
            full_list.append(sub_list)
            sub_list = list()

    global editable_full_list
    editable_full_list = full_list

    canvas.tag_bind("cat1a", "<Button-1>", lambda x: categorize(0))
    canvas.tag_bind("cat2a", "<Button-1>", lambda x: categorize(1))
    canvas.tag_bind("cat3a", "<Button-1>", lambda x: categorize(2))
    canvas.tag_bind("cat4a", "<Button-1>", lambda x: categorize(3))
    canvas.tag_bind("cat5a", "<Button-1>", lambda x: categorize(4))
    canvas.tag_bind("cat6a", "<Button-1>", lambda x: categorize(5))
    canvas.tag_bind("cat1b", "<Button-1>", lambda x: categorize(6))
    canvas.tag_bind("cat2b", "<Button-1>", lambda x: categorize(7))
    canvas.tag_bind("cat3b", "<Button-1>", lambda x: categorize(8))
    canvas.tag_bind("cat4b", "<Button-1>", lambda x: categorize(9))
    canvas.tag_bind("cat5b", "<Button-1>", lambda x: categorize(10))
    canvas.tag_bind("cat6b", "<Button-1>", lambda x: categorize(11))


# FUNCTION 2: LOAD SPECIFIC DATA BASED ON THE SELECTED CATEGORY
def categorize(args):

    save_label2.destroy() # Remove the label displayed if the user pressed saved prior to selecting a category

    global save_label # Create a label once the user presses save to indicate the data has been saved
    save_label = Label(root, text='Category ' + str(args + 1) + " Saved.", font='Helvetica 14 bold')

    global cat  # Used to store the category number being edited
    cat = args + 1

    if t.compare("end-1c", "!=", "1.0"):
        t.delete('1.0', END)
    if t2.compare("end-1c", "!=", "1.0"):
        t2.delete('1.0', END)

    for x in editable_full_list[args]:

        if args in list(range(0,6)):
            l.configure(text="Editing R1 Category " + " " + str(cat))
            l.place(relx=0.6, y=spacer, anchor=CENTER)
            t.insert(END, str(x) + '\n')
            t.place(x = start_x + rec_len,
                    y = start_y,
                    height = 6 * (rec_width - spacer) - start_y + spacer ,
                    width = 5 * (rec_len - spacer) - spacer)
        else:
            t2.insert(END, str(x) + '\n')
            l.configure(text="Editing R2 Category " + " " + str(cat - 6))
            l.place(relx=0.6, y=6* rec_width - 1.5*spacer, anchor=CENTER)
            t2.place(x=start_x + rec_len,
                     y=start_y + 8 * rec_width - 8 * spacer + 5,
                     height=6 * (rec_width - spacer) - start_y + spacer,
                     width=5 * (rec_len - spacer) - spacer)


# FUNCTION 3: WRITE DATA TO A LIST OF LISTS FOR A SPECIFIC CATEGORY
def retrieve_input():

    global input_value
    input_value = t.get("1.0", "end-1c")
    if t.compare("end-1c", "==", "1.0"):
        input_value = t2.get("1.0", "end-1c")
    dat = input_value.split("\n")
    dat = list(filter(None, dat))

    try:
        dat_idx = list(range(10*(cat - 1) + cat - 1, 10*(cat - 1) + cat + 10))

        idx = 0

        for i in dat_idx:
            final_list[i] = dat[idx]
            idx += 1

        global flat_list
        flat_list = [item for sublist in editable_full_list for item in sublist]


        for j in range(len(final_list)):
            if final_list[j] != '':
                flat_list[j] = final_list[j]



        global new_list

        new_list = [flat_list[11 * i: 11 * (i + 1)] for i in range(12)]
        for k in range(len(editable_full_list)):
            editable_full_list[k] = new_list[k]


    except NameError: pass


# FUNCTION 4: DISPLAY SAVE LABEL TO USER UPON SAVING DATA
def show_save_label():

    try:
        save_label.place(relx = 0.45, y=15 * (rec_width - spacer) + start_y + 10, anchor=CENTER)
    except NameError:
        save_label2.place(relx = 0.45, y = 15 * (rec_width - spacer) + start_y + 10, anchor=CENTER)


# FUNCTION 5: SAVE OUTPUT OF CHANGES TO FILE

def save_and_quit():

    #try: flat_list
    #except NameError:
     #   root.destroy()

    retrieve_input()

    new_file = open("resources/category_question_answer.txt", "w")
    try:
        for k in flat_list[:-1]:
            new_file.write("%s\n" % k)
            
    except NameError:
        for line in open(filename2):
            new_file.write(line)

    new_file.close()
    root.destroy()

# FUNCTION 6: QUIT DATA EDITOR
def exit_editor():

    root.destroy()


# FUNCTION 7: ALLOW USER TO SELECT THEIR OWN FILE TO IMPORT
def select_file():
    dialog = Tk()
    global isClicked
    isClicked = True
    global imported_file
    dialog.withdraw()
    imported_file = askopenfilename()
    if isClicked and imported_file != '':
        #PLACE IMPORT LABEL HERE
        l.configure(text="File Imported. Select a Category to Edit.")
        l.place(relx=0.6, y=spacer, anchor=CENTER)
        t.delete('1.0', END)
        load_data(imported_file)
    dialog.destroy()

# FUNCTION 8: RESTORE THE DEFAULT FILE INTO THE EDITOR
def restore_default():
    load_data("resources/default_do_not_delete_or_edit.txt")
    l.configure(text="Default Values Restored. Select a Category Again to Edit.")
    l.place(relx=0.6, y=spacer, anchor=CENTER)

def load_last_used():
    load_data("resources/category_question_answer.txt")
    l.configure(text="Questions from the last game have been loaded." + "\n" + "Select a Category Again to Edit.")
    l.place(relx=0.6, y=spacer, anchor=CENTER)

# DEFAULT STATE OF THE EDITOR
load_data("resources/default_do_not_delete_or_edit.txt")



root.mainloop()
