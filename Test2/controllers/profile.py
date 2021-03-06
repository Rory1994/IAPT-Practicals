#Exam Number: Y0071297

import datetime

# Initialise the countries, years and months array for use in select statement.
COUNTRIES=['United Kingdom', 'United States', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Ivory Coast', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea','South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'FYROM', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe', 'Other']
years = []
months = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]

for i in xrange(100):
    if i < 10:
        number = '0' + str(i)
    else:
        number = str(i)

    years.append(number)



@auth.requires_login(otherwise=URL('default','login'))
def profile():

    # Retrieve information for logged in user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()

    # Retrieve the number of projects and pledge a user has
    number_of_projects = len(db(db.project.username == auth._get_user_id()).select())
    number_of_pledges = len(db(db.pledges.username == auth._get_user_id()).select())


    return dict(user=user, number_of_projects=number_of_projects, number_of_pledges=number_of_pledges )

@auth.requires_login(otherwise=URL('default','login'))
def projects():

    # Retrieve information for logged in user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()

    # Queries for retrieving the project a user owns.
    open_for_pledges_projects = db((db.project.username == auth._get_user_id()) & (db.project.status  == "Open for Pledges")).select()
    not_available_projects = db((db.project.username == auth._get_user_id()) & (db.project.status  == "Not Available")).select()
    funded_projects = db((db.project.username == auth._get_user_id()) & (db.project.status  == "Funded")).select()
    not_funded_projects = db((db.project.username == auth._get_user_id()) & (db.project.status  == "Not Funded")).select()


    
    return dict(user=user, open_for_pledges_projects = open_for_pledges_projects, not_available_projects = not_available_projects,
                funded_projects = funded_projects, not_funded_projects = not_funded_projects)

@auth.requires_login(otherwise=URL('default','login'))
def pledges():

    # Retrieve information for logged in user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()

    #Retrieves all pledges made by a user
    pledges_made_by_user = db((db.pledges.username == user.id) & (db.pledge_levels.project_id == db.project.id) & (db.pledge_levels.id == db.pledges.pledge_levels_id)).select()

    return dict(user = user, pledges_made_by_user = pledges_made_by_user)

@auth.requires_login(otherwise=URL('default','login'))
def information():

    # Retrieve all personal information to do with a user.
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    bank_details = db(db.bank_details.id == user.bank_details_id).select().first()
    address = db(db.address.id == user.address_id).select().first()
    bank_address = db(db.address.id == bank_details.address_id).select().first()

    return dict(user=user,  bank_details = bank_details, address=address, bank_address=bank_address)


@auth.requires_login(otherwise=URL('default','login'))
def create():

    form_has_errors = False

    #Reset pledge levels list if coming to the create form from another page apart from step two.
    if (request.vars.coming_back_from_step_two != "True"):
         session.pledge_levels = []

    # Initialise category options
    options = ['Arts', 'Comics', 'Crafts', 'Fashion', 'Film', 'Games', 'Music', 'Photography', 'Technology']


    # Create form for create step 1
    form= FORM(FIELDSET(

                        DIV(LABEL('Project Title:', _for='project_title'),
                            INPUT(_id='project_title', _name='project_title', _type='text', _class='span6',_style="display: block;",requires=IS_NOT_EMPTY(error_message=T("Title must be entered"))),

                            LABEL('Short Project Description:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be at most 120 characters. Briefly sum up the project",href="#", rel='tooltip'), _for='short_project_description'),
                            TEXTAREA(_id='short_project_description', _name='short_project_description', _rows = '2', _maxlength = "120", _class='span6',_style="display: block;",requires=[IS_NOT_EMPTY(error_message=T("Short description must be entered")), IS_LENGTH(120, error_message=T("Must be at most 120 characters"))]),

                            LABEL('Category:', _for='category'),
                            SELECT(*options, _name='category', _id='category',_class='span6',_style="display: block;" ,requires= [IS_IN_SET(options, error_message=T("Category from list must be chosen"))]),

                            _class='controls control-group'),


                            DIV(LABEL('Funding Goal (in whole GBPs):', A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Funding goal must be a whole number in Pound sterling (£). For instance, £99.50 would NOT be valid",href="#", rel='tooltip'), _for='funding_goal'),
                            INPUT(_id='funding_goal', _name='funding_goal', _type='text', _class='span6',_style="display: block;",requires=[IS_NOT_EMPTY(error_message=T("Funding goal must be entered")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),

                            LABEL('Long Description of Project Goals:', _for='long_description'),
                            TEXTAREA(_id='long_description', _name='long_description', _rows = '20', _class='span9',_style="display: block;",requires=IS_NOT_EMPTY(error_message=T("Long description must be entered"))),

                            LABEL('Project Story:', _for='project_story'),
                            TEXTAREA(_id='project_story', _name='project_story',_cols = '50', _rows = '20', _class='span9',_style="display: block;",requires=IS_NOT_EMPTY(error_message=T("Project story must be entered")))

                            ,_class='controls control-group'),



                         BUTTON("Move on to step 2 and start adding pledges ",I(_class='icon-arrow-right icon-white'), _type='submit', _class='btn btn-primary btn-large')


    ))

    # Prepopulate form if coming back from step 2
    if (request.vars.coming_back_from_step_two == "True"):
        form.vars.project_title = session.create.project_title
        form.vars.short_project_description = session.create.short_project_description
        form.vars.category = session.create.category
        form.vars.funding_goal = session.create.funding_goal
        form.vars.long_description = session.create.long_description
        form.vars.project_story = session.create.project_story




    if form.process().accepted:
        #Pass form variables to next step
        session.create = request.vars
        redirect(URL('profile','create_step2'))

    elif form.errors:
        form_has_errors = True
        response.flash = form.errors



    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()


    return dict(user=user, form=form, form_has_errors = form_has_errors)

@auth.requires_login(otherwise=URL('default','login'))
def create_step2():

    # Retrieve all information about a user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()

    # Binrg forward request variables from previous step
    if session.create:
        request.vars.update(session.create)

    # Create pledge adding form
    form = FORM(DIV(A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Ensure that the pledge amount is a whole number. Values such as £4.50 are not allowed.",href="#", rel='tooltip'),INPUT(_id='pledge_amount', _name='pledge_amount', _type='text', _placeholder = "£", _class='span2',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),
            TEXTAREA(_placeholder = 'Reward', _id='pledge_reward', _name='pledge_reward',_cols = '50', _rows = '5', _class='span5', requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
           _class="controls control-group" ), INPUT(_type='submit', _class='btn btn-info btn-large', _value='Add Reward'))

    # Create button that takes you forward to step 3
    go_to_step_3 = FORM(DIV(BUTTON("Move on to step 3 and add a picture ",I(_class='icon-arrow-right icon-white'), _type='submit', _class='btn btn-primary btn-block btn-large')))

    if form.process(formname='form_one').accepted:
        session.pledge_levels.append([request.vars.pledge_amount, request.vars.pledge_reward])

    if go_to_step_3.process(formname='form_two').accepted:
        # Ensures atleast one pledge has been added by user. If it has then go forward to step 3.
        if len(session.pledge_levels) <1:
            response.flash = DIV("At least one pledge must be added for a bootable to be created", _class="alert alert-error")

        else:
            session.create = request.vars
            redirect(URL('profile','create_step3'))



    return dict(pledge_levels = session.pledge_levels, form = form, user = user, go_to_step_3 = go_to_step_3)






@auth.requires_login(otherwise=URL('default','login'))
def create_step3():

    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()

    #Bring forward request variables
    if session.create:
        request.vars.update(session.create)

    if session.pledge_levels:
        request.vars.update({'pledge_levels':session.pledge_levels})

    response.flash = request.vars

    # Creat picture adding form
    form= FORM(LABEL('Project Image:', _for='image'),DIV(
                INPUT(_id='image', _name='image', _type='file', _class='span6',_style="display: block;",
                requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))), _class="controls control-group"),
                 INPUT(_type='submit', _class='btn btn-primary btn-large btn-block', _value="Create Project"))

    if form.process().accepted:

        # INsert project into database
        project = db.project.insert(username = auth._get_user_id, short_description = request.vars.short_project_description,
                                     status='Not Available', image = request.vars.image, category = request.vars.category,
                                     funding_raised = 0, story = request.vars.project_story, opened_for_pledges_date = request.now,
                                     funding_target = int(request.vars.funding_goal), title = request.vars.project_title,
                                     long_description = request.vars.long_description)

        # INsert pledge levels into database
        for pledge_level in request.vars.pledge_levels:

            db.pledge_levels.insert(project_id = project.id, pledge_amount = int(pledge_level[0]), reward = pledge_level[1])

        session.flash = DIV( H4("Congratulations, You successfully created the project '" +  request.vars.project_title + "'"),_class="alert alert-success")
        session.create = None
        session.pledge_levels = None


        redirect(URL('profile', 'projects'))



    return dict(user=user, form=form)


@auth.requires_login(otherwise=URL('default','login'))
def change_password():

    #CReate change password form
    form = FORM(FIELDSET(
                        LEGEND('Change Password'),
                        DIV(
                            LABEL('New Password:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Password must be at least six characters long",href="#", rel='tooltip') ,_for='new_password'),INPUT(_id='new_password', _name='new_password', _type='password', _class='span4',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_LENGTH(minsize=6, error_message="Password must be at least 6 characters")]),
                            LABEL('Confirm New Password:', _for='confirm_new_password'),INPUT(_id='confirm_new_password', _name='confirm_new_password', _type='password', _class='span4'
                            , requires=[IS_EQUAL_TO(request.vars.confirm_new_password, error_message=T("Passwords do not match")), IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))]),
                            _class='controls control-group'),

                        INPUT(_type='submit', _class='btn btn-primary', _value='Change Password')
    ))

    if form.process().accepted:

        # Changes users password
        user = db(db.auth_user.id == auth._get_user_id()).select().first()
        user.update_record(password = db.auth_user.password.validate(form.vars.new_password)[0])

        response.flash = DIV('Password has been successfully changed', _class="alert alert-success")

    elif form.errors:
         response.flash = DIV("Passwords either don't match or aren't long enough or don't match", _class="alert alert-error")

    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()


    return dict(form = form, user = user)

@auth.requires_login(otherwise=URL('default','login'))
def edit_information():

    form_has_errors = False

    #Retrieve users information
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    bank_details = db(db.bank_details.id == user.bank_details_id).select().first()
    address = db(db.address.id == user.address_id).select().first()
    bank_address = db(db.address.id == bank_details.address_id).select().first()

    # Create edit information form
    form= FORM(FIELDSET(

                        LEGEND('Personal Information'),
                        DIV(LABEL('First Name:', _for='first_name'),INPUT(_id='first_name', _name='first_name', _type='text', _class='span4',_style="display: block;"),
                            LABEL('Last Name:', _for='last_name'),INPUT(_id='last_name', _name='last_name', _type='text', _class='span4',_style="display: block;")
                            ,_class='controls control-group'),


                        DIV( LABEL('Date of Birth:', A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Example: 25/02/1994",href="#", rel='tooltip')),
                             INPUT( _name='dob', _type='text',_placeholder = ('dd/mm/yyyy'),_maxlength='10', _class='date',_style="display: block;")
                             ,_class="controls controls-row"),

                        LEGEND('Home Address'),
                        DIV(LABEL('Street:', _for='street'),INPUT(_id='street', _name='street', _type='text', _class='span4',_style="display: block;"),
                            LABEL('City:', _for='city'),INPUT(_id='city', _name='city', _type='text', _class='span4',_style="display: block;"),
                            LABEL('Postcode:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be in the format **** ***. Example: IG90 7GH",href="#", rel='tooltip'), _for='postcode'),INPUT(_id='postcode', _name='postcode', _type='text', _class='span4',_style="display: block;"),
                            LABEL('Country:', A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Choose a country from the list",href="#", rel='tooltip'),_for='country'),SELECT(*COUNTRIES, _id='country', _name='country',_style="display: block;")
                            ,_class='controls control-group'),

                        LEGEND('Billing Information'),
                        DIV(LABEL('Card Number:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be a 12 digits consisting of just numbers. No spaces should be included.",href="#", rel='tooltip'), _for='card_number'),INPUT(_id='card_number', _name='card_number', _type='text',_maxlength='12' ,_class='span4',_style="display: block;"),
                            LABEL('Security Code:', A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be 3 digits consisting of just numbers",href="#", rel='tooltip'), _for='security_code'),INPUT(_id='security_code', _name='security_code', _type='text',_maxlength='3', _class='span4',_style="display: block;")
                            ,_class='controls control-group'),

                        DIV(
                            LABEL('Expiry Date:', A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Select a valid date in the format mm/yy",href="#", rel='tooltip')),
                            SELECT(*months, _value='mm', _name='expiry_date_month', _id='expiry_date_month' ),
                            SPAN(' / '),
                            SELECT(*years, _value='yy', _name='expiry_date_year', _id='expiry_date_year')
                            , _class='controls controls-row'),

                        LEGEND('Billing Address'),
                        DIV(LABEL(INPUT(_id='billing_checkbox', _name='billing_checkbox', _value='yes', _onclick='javascript:toggleAddressAvailibility();', _type='checkbox' ), 'Same as Home Address',_class='checkbox'),
                            DIV(LABEL('Street:', _for='billing_street'),INPUT( _name='billing_street', _type='text', _class='span4',_style="display: block;"), _id='billing_street'),
                            DIV(LABEL('City:', _for='billing_city'),INPUT( _name='billing_city', _type='text', _class='span4',_style="display: block;"), _id='billing_city'),
                            DIV(LABEL('Postcode:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be in the format **** ***. Example: IG90 7GH",href="#", rel='tooltip'), _for='billing_postcode'),INPUT( _name='billing_postcode', _type='text', _style="display: block;", _class='span4'), _id='billing_postcode'),
                            DIV(LABEL('Country:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Choose a country from the list",href="#", rel='tooltip'), _for='billing_country'),SELECT(*COUNTRIES, _name='billing_country'), _id='billing_country')
                            ,_class='controls control-group last_form_section'),

                         INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Confirm Changes')


    ))

    #Prepopulate form
    form.vars.first_name = user.first_name
    form.vars.last_name = user.last_name
    form.vars.dob = generate_correct_date_format(user.birthdate)
    form.vars.street = address.street
    form.vars.city = address.city
    form.vars.country = address.country
    form.vars.postcode = address.postcode
    form.vars.card_number = bank_details.card_number
    form.vars.security_code = bank_details.security_code

    expiry_date = bank_details.expiry_date.partition("/")

    form.vars.expiry_date_month = expiry_date[0]
    form.vars.expiry_date_year = expiry_date[2]
    form.vars.billing_street = bank_address.street
    form.vars.billing_city = bank_address.city
    form.vars.billing_country = bank_address.country
    form.vars.billing_postcode = bank_address.postcode


    if form.process(onvalidation=edit_information_validation).accepted:

        new_home_address_was_added = False

        ##UPDATE Personal Info
        if request.vars.first_name != user.first_name:
            user.update_record(first_name = request.vars.first_name)

        if request.vars.last_name != user.last_name:
            user.update_record(last_name = request.vars.last_name)

        if request.vars.dob != user.birthdate:
            date_of_birth = request.vars.dob.split('/')
            user.update_record(birthdate= datetime.date(int(date_of_birth[2]), int(date_of_birth[1]), int(date_of_birth[0])))

        ## UPDATE address

        if (user.address_id == bank_details.address_id):
            number_of_banks_with_same_address_limit = 1
        else:
            number_of_banks_with_same_address_limit = 0

        number_of_users_using_the_same_address = len(db(db.auth_user.address_id == user.address_id).select())
        number_of_bank_details_using_the_same_address = len(db(db.bank_details.address_id == user.address_id).select())

        if (number_of_users_using_the_same_address > 1) or (number_of_bank_details_using_the_same_address >  number_of_banks_with_same_address_limit):

            if request.vars.street != address.street or request.vars.city != address.city or request.vars.country != address.country or request.vars.postcode != address.postcode:
                new_address_id = db.address.insert(street = request.vars.street, city = request.vars.city, country = request.vars.country, postcode = request.vars.postcode)
                user.update_record(address_id = new_address_id)
                new_home_address_was_added = True



        else:

            if request.vars.street != address.street:
                address.update_record(street = request.vars.street)

            if request.vars.city != address.city:
                address.update_record(city = request.vars.city)

            if request.vars.country != address.country:
                address.update_record(country = request.vars.country)

            if request.vars.postcode != address.postcode:
                address.update_record(postcode = request.vars.postcode)


        ## UPDATE BANK DETAILS
        number_of_users_using_the_same_card = len(db(db.auth_user.bank_details_id == user.bank_details_id).select())

        expiry_date = request.vars.expiry_date_month + "/" + request.vars.expiry_date_year

        if number_of_users_using_the_same_card > 1:

            if request.vars.card_number != bank_details.card_number or request.vars.security_code != bank_details.security_code or expiry_date != bank_details.expiry_date:
                new_bank_details_id = db.bank_details.insert(card_number = request.vars.card_number, security_code = request.vars.security_code,
                                    expiry_date = expiry_date)
                user.update_record(bank_details_id = new_bank_details_id)



        else:

            if request.vars.card_number != bank_details.card_number:
                bank_details.update_record(card_number= request.vars.card_number)

            if request.vars.security_code != bank_details.security_code:
                bank_details.update_record(security_code = request.vars.security_code)

            if expiry_date != bank_details.expiry_date:
                bank_details.update_record(expiry_date = expiry_date)


        ## UPDATE BANK_ADDRESS

        if request.vars.billing_checkbox =='yes':

            if new_home_address_was_added:
                bank_details.update_record(address_id = new_address_id)

            else:
                bank_details.update_record(address_id = address.id)

        else:

            if (request.vars.street == request.vars.billing_street) and (request.vars.city == request.vars.billing_city) and \
            (request.vars.country == request.vars.billing_country) and (request.vars.postcode == request.vars.billing_postcode):

                if new_home_address_was_added:
                    bank_details.update_record(address_id = new_address_id)

                else:
                    bank_details.update_record(address_id = address.id)

            else:

                if (user.address_id == bank_details.address_id):
                    number_of_users_with_same_address_limit = 1
                else:
                    number_of_users_with_same_address_limit = 0

                number_of_users_using_the_same_address = len(db(db.auth_user.address_id == bank_address.id).select())
                number_of_bank_details_using_the_same_address = len(db(db.bank_details.address_id == bank_address.id).select())

                if (number_of_users_using_the_same_address > number_of_users_with_same_address_limit) or (number_of_bank_details_using_the_same_address > 1):
                     if request.vars.billing_street != bank_address.street or request.vars.billing_city != bank_address.city or\
                        request.vars.billing_country != bank_address.country or request.vars.billing_postcode != bank_address.postcode:

                        new_bank_address_id = db.address.insert(street = request.vars.billing_street, city = request.vars.billing_city,
                                             country = request.vars.billing_country, postcode = request.vars.billing_postcode)

                        bank_details.update_record(address_id = new_bank_address_id)

                else:

                    if request.vars.billing_street != bank_address.street:
                        address.update_record(street = request.vars.billing_street)

                    if request.vars.billing_city != bank_address.city:
                        address.update_record(city = request.vars.billing_city)

                    if request.vars.billing_country != bank_address.country:
                        address.update_record(country = request.vars.billing_country)

                    if request.vars.billing_postcode != bank_address.postcode:
                        address.update_record(postcode = request.vars.billing_postcode)

        session.flash = DIV( H4("You successfully changed your information"),_class="alert alert-success")
        redirect(URL('information'))

        #if (request.vars.expiry_date_month != expiry_date[0]) or (request.vars.expiry_date_year != expiry_date[2]):

    elif form.errors:
        form_has_errors = True
        response.flash = form.errors


    return dict(user = user, form = form, form_has_errors = form_has_errors)

def generate_correct_date_format(date):

    #Given a date object its converts it into a string in the format dd/mm/yyyy

    date_string = ""
    if date.day < 10:
        date_string += "0" + str(date.day) + "/"
    else:
        date_string += str(date.day) + "/"

    if date.month < 10:
        date_string += "0" + str(date.month) + "/"
    else:
        date_string += str(date.month) + "/"

    date_string += str(date.year)

    return date_string


def edit_information_validation(form):

    #Ensure first name is entered
    if form.vars.first_name == "":
        form.errors.first_name = "First name must be entered"

    #Ensure last name is entered
    if form.vars.last_name == "":
        form.errors.last_name = "Last name must be entered"

    #Ensure date is in correct format
    date_validator = IS_DATE(format='%d/%m/%Y', error_message=T("Date should be given as dd/mm/yyyy"))
    if date_validator(form.vars.dob)[1] is not None:
        form.errors.dob = "Date should be given as dd/mm/yyyy"

    # Ensure street is entered
    if form.vars.street == "":
        form.errors.street = "Street must be entered"

    #Ensure city is entered
    if form.vars.city == "":
        form.errors.city = "City must be entered"

    # Ensure country is entered
    if form.vars.country == "":
        form.errors.country = "Country must be entered"

    # Ensure postcode is in correct format
    postcode_validator =  IS_MATCH('^[A-Z0-9]{4} [A-Z0-9]{3}$', error_message="Postcode is not valid. Must be split into a block of 4 characters and a block of 3 characters. Example: IG90 7GH" )
    if postcode_validator(form.vars.postcode)[1] is not None:
        form.errors.postcode = postcode_validator(form.vars.postcode)[1]

    #Ensure security code is length 3
    security_code_validator = IS_MATCH('^[0-9]{3}$', error_message='Security code must contain 3 numbers')
    if security_code_validator(form.vars.security_code)[1] is not None:
        form.errors.security_code = security_code_validator(form.vars.security_code)[1]

    #Ensure card number is length 12.
    card_number_validator = IS_MATCH('^[0-9]{12,12}$', error_message="Card number must be 12 digits long. No spaces should be included" )
    if card_number_validator(form.vars.card_number)[1] is not None:
        form.errors.card_number = card_number_validator(form.vars.card_number)[1]

    if form.vars.billing_checkbox != "yes":

        #Ensures billing street is entered
        if form.vars.billing_street =="":
            form.errors.billing_street = "Street must be entered"

        # Ensures billing city is entered
        if form.vars.billing_city =="":
            form.errors.billing_city = "City must be entered"

        # Ensures billing country is entered
        if form.vars.billing_country =="":
            form.errors.billing_country = "Country must be entered"

        #Ensures billing postcode
        if form.vars.billing_postcode =="":
            form.errors.billing_postcode = "Postcode must be entered"

        #Ensures postcode in correct format
        if postcode_validator(form.vars.billing_postcode)[1] is not None:
            form.errors.billing_postcode = postcode_validator(form.vars.billing_postcode)[1]

    if form.vars.expiry_date_month not in months or form.vars.expiry_date_year not in years:
        form.errors.expiry_date_year = "Expiry Date must be entered"






@auth.requires_login(otherwise=URL('default','login'))
def view_project():

    project = None
    project_id = request.args(0)
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    #Retrieve project from db
    projects = db((db.project.username == auth._get_user_id) & (db.project.id == project_id) ).select()

    # If project isnt owned by user redirect
    if len(projects) < 1:
        redirect(URL('profile', 'profile'))

    else:
        project = projects.first()
        #If project shouldnt be able to be viewed in this manner, redirect.
        if project.status != "Not Available":
             redirect(URL('profile', 'profile'))


    return dict(project = project, user = user)

def delete_pledge():
    #deletes a particular pledge level for a project
    db(db.pledge_levels.id == request.vars.id).delete()
    session.flash = DIV( H4("You successfully deleted a pledge level"),_class="alert alert-error")
    redirect(URL('rewards', args=request.vars.project_id), client_side=True)

@auth.requires_login(otherwise=URL('default','login'))
def rewards():

    form=None
    project = None
    pledge_levels = None
    project_id = request.args(0)
    #Retrieve user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    #Retrieve project
    projects = db((db.project.username == auth._get_user_id) & (db.project.id == project_id) ).select()

    # If project doesnt belong to user, redirect
    if len(projects) < 1:
        redirect(URL('profile', 'profile'))

    else:
        project = projects.first()

        if project.status != "Not Available":
             redirect(URL('profile', 'profile'))

        #Create add pledge levels form
        form = FORM(DIV(A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Ensure that the pledge amount is a whole number. Values such as £4.50 are not allowed.",href="#", rel='tooltip'),INPUT(_id='pledge_amount', _name='pledge_amount', _type='text', _placeholder = "£", _class='span2',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),
                TEXTAREA(_placeholder = 'Reward', _id='pledge_reward', _name='pledge_reward',_cols = '50', _rows = '5', _class='span5', requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
               _class="controls control-group" ), INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Add Reward'))

        if form.process().accepted:
            #Insert pledge level into database
            db.pledge_levels.insert(project_id = project.id, pledge_amount = int(request.vars.pledge_amount), reward = request.vars.pledge_reward)
            response.flash = DIV( H4("You successfully added a pledge level"),_class="alert alert-success")





        pledge_levels = db(db.pledge_levels.project_id == project_id).select(orderby=db.pledge_levels.pledge_amount)

    return dict(pledge_levels = pledge_levels, form = form, user = user, project=project)

@auth.requires_login(otherwise=URL('default','login'))
def change_picture():

    form=None
    project = None
    project_id = request.args(0)
    #Retrieve user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    #Retrieve project
    projects = db((db.project.username == auth._get_user_id) & (db.project.id == project_id) ).select()

    #If users doesnt own project, redirect
    if len(projects) < 1:
        redirect(URL('profile', 'profile'))

    else:

        project = projects.first()

        if project.status != "Not Available":
             redirect(URL('profile', 'profile'))

        #Create change picture form
        form = FORM(LABEL('New Image:', _for='image'),
                INPUT(_id='image', _name='image', _type='file', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Change Picture'))

        if form.process().accepted:
            #UPdate record with new image
            project.update_record(image = request.vars.image)
            session.flash = DIV( H4("You successfully changed the project picture"),_class="alert alert-success")
            redirect(URL('profile','view_project', args=project.id))


    return dict(form = form, user = user, project=project)

@auth.requires_login(otherwise=URL('default','login'))
def edit_project():

    form_has_errors = False

    options = ['Arts', 'Comics', 'Crafts', 'Fashion', 'Film', 'Games', 'Music', 'Photography', 'Technology']


    form=None
    project = None
    project_id = request.args(0)
    #Retrieve user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    #Retrieve Project
    projects = db((db.project.username == auth._get_user_id) & (db.project.id == project_id) ).select()

    #If user didn't own project redirect.
    if len(projects) < 1:
        redirect(URL('profile', 'profile'))

    else:
        project = projects.first()

        #If project is live and can't be edited, redirect
        if project.status != "Not Available":
             redirect(URL('profile', 'profile'))


        #Create edit project form
        form= FORM(FIELDSET(

                        DIV(LABEL('Project Title:', _for='project_title'),
                            INPUT(_id='project_title', _name='project_title', _type='text', _class='span6',requires=IS_NOT_EMPTY(error_message=T("Project title must be entered"))),

                            LABEL('Short Project Description:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be at most 120 characters. Briefly sum up the project",href="#", rel='tooltip') ,_for='short_project_description'),
                            TEXTAREA(_id='short_project_description', _name='short_project_description', _cols = '50', _rows = '5', _class='span6',requires=[IS_NOT_EMPTY(error_message=T("Short project description must be entered")), IS_LENGTH(120, error_message=T("Must be at most 120 characters"))]),

                            LABEL('Category:', _for='category'),
                            SELECT(*options, _name='category', _id='category', _class="span6", requires= [IS_IN_SET(options, error_message=T("Category from list must be chosen"))])


                            ,_class='controls control-group'),


                            DIV(LABEL('Funding Goal (in GBPs):',  A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Funding goal must be a whole number in Pound sterling (£). For instance, £99.50 would NOT be valid",href="#", rel='tooltip') ,_for='funding_goal'),
                            INPUT(_id='funding_goal', _name='funding_goal', _type='text', _class='span6',requires=[IS_NOT_EMPTY(error_message=T("Funding goal must be entered")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),

                            LABEL('Long Description of Project Goals:', _for='long_description'),
                            TEXTAREA(_id='long_description', _name='long_description',_cols = '50', _rows = '10', _class='span6',requires=IS_NOT_EMPTY(error_message=T("Long description must be entered"))),

                            LABEL('Project Story:', _for='project_story'),
                            TEXTAREA(_id='project_story', _name='project_story',_cols = '50', _rows = '10', _class='span6',requires=IS_NOT_EMPTY(error_message=T("Project story must be entered")))

                            ,_class='controls control-group'),


                         INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Confirm Changes')

         ))

        #Prepopulate form
        form.vars.project_title = project.title
        form.vars.short_project_description = project.short_description
        form.vars.category = project.category
        form.vars.funding_goal = int(project.funding_target)
        form.vars.long_description = project.long_description
        form.vars.project_story = project.story

        if form.process().accepted:

        #Update project information

            if request.vars.project_title != project.title:
                project.update_record(title = request.vars.project_title)

            if request.vars.short_project_description != project.short_description:
                project.update_record(short_description = request.vars.short_project_description)

            if request.vars.category!= project.category:
                project.update_record(category = request.vars.category)

            if request.vars.funding_goal != project.funding_target:
                project.update_record(funding_target = int(request.vars.funding_goal))

            if request.vars.long_description != project.long_description:
                project.update_record(long_description = request.vars.long_description)

            if request.vars.project_story != project.story:
                project.update_record(story= request.vars.project_story)

            session.flash = DIV( H4("You successfully changed your project information"),_class="alert alert-success")

            redirect(URL('profile','view_project', args=project.id))

        elif form.errors:
            form_has_errors = True
            response.flash = form.errors





    return dict(form = form, user = user, project=project, form_has_errors = form_has_errors)

def delete_project():
    #Deletes a specific project
    db(db.project.id == request.vars.project_id).delete()
    session.flash = DIV( H4(" You successfully deleted the project"),_class="alert alert-error")
    redirect(URL('profile','projects', args=request.vars.project_id), client_side=True)



@auth.requires_login(otherwise=URL('default','login'))
def confirm_open_for_pledges():

    form=None
    project = None
    project_id = request.args(0)
    #Retrieve user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    #Retrieve project
    projects = db((db.project.username == auth._get_user_id) & (db.project.id == project_id) ).select()

    # If users doesnt own project don't allow them to do this
    if len(projects) < 1:
        redirect(URL('profile', 'profile'))

    else:
        project = projects.first()

        # If project is funded or already open, redirect
        if (project.status != "Not Available") and (project.status != "Not Funded"):
             redirect(URL('profile', 'projects'))

        # Create open for pledges form.
        form= FORM(INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Yes, open project for pledges'))

        if form.process().accepted:
            #Update project status
             project.update_record(status = "Open for Pledges", open_for_pledges_date = request.now)
             session.flash = DIV( H4("You successfully opened '" + project.title + "' for pledges" ),_class="alert alert-success")
             redirect(URL('profile', 'projects', args=request.vars.project_id))

    return dict(form = form, user = user, project=project)

@auth.requires_login(otherwise=URL('default','login'))
def close_from_pledges():

    form=None
    project = None
    project_id = request.args(0)
    #Retrieve user
    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    #Retrieve project
    projects = db((db.project.username == auth._get_user_id) & (db.project.id == project_id) ).select()

    #If user doesnt own project, redirect
    if len(projects) < 1:
        redirect(URL('profile', 'profile'))

    else:
        project = projects.first()

        #Redirect if not open for pledges
        if project.status != "Open for Pledges":
             redirect(URL('profile', 'projects'))

        #Create close from pledges form.
        form= FORM(INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Yes, close project from pledges'))

        if form.process().accepted:
            #If funded , move to funded, if not, move to not funded
             if project.funding_target > project.funding_raised:
                 project.update_record(status = "Not Funded")
             else:
                 project.update_record(status = "Funded")

             session.flash = DIV( H4("You successfully closed '" + project.title + "' for pledges" ),_class="alert alert-error")
             redirect(URL('profile', 'projects', args=request.vars.project_id))

    return dict(form = form, user = user, project = project)











