from message import Message

messages = {}
messages[1] = Message("A.Tutor@grandwich.ac.uk", "Hello", "B.Tutor@grandwich.ac.uk", "How is the course going?", 2)
messages[2] = Message("B.Tutor@grandwich.ac.uk", "Re: Hello", "A.Tutor@grandwich.ac.uk",
                      "> How is the course going?\n\nBrilliant, thanks. The students are all fantastic and are going to get top marks in their coursework.",
                      2)
messages[3] = Message("A.Friend@kmail.com", "Coffee", "A.Tutor@grandwich.ac.uk",
                      "You're working too hard - fancy meeting for coffee?.", 5)
messages[4] = Message("A.Tutor@grandwich.ac.uk", "Exam", "C.Tutor@grandwich.ac.uk",
                      "I have nearly finished writing the exam - I hope the students have revised hard.", 4)
messages[5] = Message("A.Student@grandwich.ac.uk", "Timetable", "A.Tutor@grandwich.ac.uk",
                      "Dear Tutor,\n\nhelp!!! my timetable is rubbish - i cant understand it!!! please tell me what to do?\n\nfrom A.Student", 0)
messages[6] = Message("A.Tutor@grandwich.ac.uk", "Re: Timetable", "A.Student@grandwich.ac.uk",
                      "Please follow the advice on Moodle - all will be clear.", 0)
messages[7] = Message("A.Student@grandwich.ac.uk", "Re: Timetable", "A.Tutor@grandwich.ac.uk", "thx :)", 0)


def list_all(label=None):
    output = "ID Priority From                      Label Subject\n" \
             "== ======== ====                      ===== =======\n"
    for message_id in messages:
        message = messages[message_id]
        if label is not None and (len(label) == 0 or label not in message.label):
            continue
        output += f"{message_id:2d} {message.info()}\n"
    return output


def get_sender(message_id):
    try:
        message = messages[message_id]
        return message.sender
    except KeyError:
        return None


def get_recipient(message_id):
    try:
        message = messages[message_id]
        return message.recipient
    except KeyError:
        return None


def get_subject(message_id):
    try:
        message = messages[message_id]
        return message.subject
    except KeyError:
        return None


def get_content(message_id):
    try:
        message = messages[message_id]
        return message.content
    except KeyError:
        return None


def get_priority(message_id):
    try:
        message = messages[message_id]
        return message.priority
    except KeyError:
        return -1


def set_priority(message_id, priority):
    try:
        message = messages[message_id]
        message.priority = priority
    except KeyError:
        return


def get_unread(message_id):
    try:
        message = messages[message_id]
        return message.unread
    except KeyError:
        return -1


def set_label(message_id, label):
    try:
        message = messages[message_id]
        message.label = label
    except KeyError:
        return


def set_unread(message_id, unread):
    try:
        message = messages[message_id]
        message.unread = unread
    except KeyError:
        return


def delete_message(message_id):
    messages.pop(message_id)


def new_message(sender, recipient, subject, content):
    # find the next empty message_id
    message_id = 0
    for message_id in messages:
        continue
    message_id += 1
    messages[message_id] = Message(sender, subject, recipient, content, 0)
