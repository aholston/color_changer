from flask import Flask, render_template, redirect, session, request
app = Flask(__name__)
app.secret_key = "ThisIsSecret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/color_change', methods=['POST'])
def color_change():
    # if field left empty, make the value highest possible
    if request.form['red'] == '':
        session['red'] = 'ff'
    else:
        session['red'] = int(request.form['red'])
    if request.form['green'] == '':
        session['green'] = 'ff'
    else:
        session['green'] = int(request.form['green'])
    if request.form['blue'] == '':
        session['blue'] = 'ff'
    else:
        session['blue'] = int(request.form['blue'])

        # establish variables for hex values 10-15, and for the final hex value
        # establish a dictionary to hold the three values before concatenation
    color_vals = ['A', 'B', 'C', 'D', 'E', 'F']
    color_dict = {}
    hex_val = ''
    # establish a function that will change a number 10 or greater to it's corresponding hex letter
    def num_to_let(val):
        idx = 0
        newVal1 = ''
        for y in range(10, val+1):
            newVal1 = color_vals[idx]
            idx += 1
        return newVal1

    for x in session:
        # skip session indexes that don't hold form values
        if x != 'y' and x != 'x':
            # make sure current session index is a number and not 'ff'
            if type(session[x]) == int:
                # change session index to pairs digits for rgba. ex: 5 turns to 05, 255 turns into 1515
                session[x] = str(session[x] / 16) + str(session[x] % 16)

                # if half of session index is a pair, we have to change it to the corresponding letter value
                if len(session[x]) % 2 == 0 and int(session[x][0:len(session[x])/2]) > 9:
                    # grab the first two numbers of the session index and store them in num
                    num = int(session[x][0:len(session[x])/2])
                    newVal = num_to_let(num)
                    # take the new letter value and prepend it to the beginning of the session index
                    session[x] = newVal + session[x][len(session[x])/2:]
                    # repeat with back 2 numbers
                    if len(session[x][1:]) > 1:
                        num = int(session[x][1:])
                        newVal = num_to_let(num)
                        session[x] = session[x][:1] + newVal
                        color_dict[x] = session[x]

                # work with 3 digit numbers
                elif len(session[x]) % 2 == 1:
                    # check if the first two numbers are the pair, if they are, repeat above process
                    if int(session[x]) / 16 > 9:
                        num = int(session[x][0:len(session[x])/2 + 1])
                        newVal = num_to_let(num)
                        session[x] = newVal + session[x][len(session[x]/2-1):]
                        color_dict[x] = session[x]
                    # if the last two numbers are the pair, repeat above process
                    else:
                        num = int(session[x][len(session[x])/2:])
                        newVal = num_to_let(num)
                        session[x] = session[x][0:1] + newVal
                        color_dict[x] = session[x]
                # if the session index is only 2 numbers, store them in the dictionary
                else:
                    color_dict[x] = session[x]

    # iterate through dictionary and store all values concatenated into one string
    # this string is used as background-color value in index.html
    for key,value in color_dict.iteritems():
        hex_val += value


    return render_template('index.html', hex_val=hex_val)


app.run(debug=True)
