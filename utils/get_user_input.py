""" Get input from user in a robust way (they can make and correct
mistakes before goin on) """

def get_user_input(message,prompt,choices):

    """Gets terminal input from user given 

      message: a long message to print first,
      prompt : a short message to ask for something, 
      choices: and a list of valid user responses.  

    E.g.:

      msg = <a long, perhaps muti-line text string>
      ans = get_user_input(msg,'Please choose:',['a','b','c'])

    This will only return characters included in the choices set
    and won't return until one of them is provided.

    Include "" as a choice if you want return to be a choice.

    If prompt = '', the choices should be full words and then only 
    the first letters of those words will be shown as the choices 
    the user can type only that instead of the whole
    word.

    E.g.:

      go_nogo = get_user_input("","",['Proceed','Re-enter','Quit?'])
    """


    not_done = True

    while not_done:

        print(message)

        choice_str = ''
        for cc in choices:
            if choice_str != '':
                choice_str += ','
            if cc != '':
                choice_str += cc

        if prompt != "":

            question = prompt+" ["
            question += choice_str
            question += "] "

            ans = input(question)

            if ans not in choices:
                print('\n\n"'+ans + '" is not in '+choice_str+'\n')
            else:
                not_done = False

        else: # if no prompt, use first letters of choices as choices

            nn = 1
            question = ''
            first_letters = ''
            new_choices = []
            for cc in choices:
                if question != '': # not first time
                    if nn == len(choices) - 1:
                        question += " or "
                    else:
                        question += ", "
                question += cc
                if first_letters != '':
                    first_letters += ','
                first_letters += cc[0].lower()
                new_choices.append(cc[0].lower())
                new_choices.append(cc[0].upper())

            question += " ["
            question += first_letters
            question += "] "

            ans = input(question)

            if ans not in new_choices:
                print('\n\n"'+ans + '" is not in '+first_letters+'\n')
            else:
                not_done = False

    return ans


def get_verified_input(default, message):

    """ Get a string from the user but make them press return one more
    time to confirm before going on.

    example:

        test_to_run = get_verified_input(test_to_run,
            "Please enter a name for the new test directory ")
    """


    not_done = True

    if default != '':
        print(message)
        ans = input('or press return to accept "'+default+'" ')

        if ans == '':
            not_done = False;
            ans = default

    else:
        ans = input(message+' ')

    while not_done:

        print('You entered "'+ans+'"')

        go_nogo = input('Press return to go on or enter something new: ')
        if go_nogo == '':
            not_done = False;
        else:
            ans = go_nogo

    return ans

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'
