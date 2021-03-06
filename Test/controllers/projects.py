#Exam Number: Y0071297

def preview_project():

    able_to_pledge = False
    project_id = request.args(0)
    #Retrieve project
    project = db(db.project.id == project_id).select().first()

    #If user doesnt own project redirect
    if auth._get_user_id() != project.username:
        redirect(URL('default', 'index'))

    #calculate the percentage of goal achieved.Also retrieve pledge levels and pledges made on project.
    percentage_completed = int((float(project.funding_raised)/float(project.funding_target))*100)
    pledge_levels = db(db.pledge_levels.project_id ==project_id).select(orderby=db.pledge_levels.pledge_amount)
    pledges_made_on_project = db((db.pledge_levels.project_id == project_id)  & (db.pledge_levels.id == db.pledges.pledge_levels_id)).select()




    return dict(project = project, percentage_completed = percentage_completed, pledge_levels = pledge_levels,
                pledges_made_on_project = pledges_made_on_project, able_to_pledge = able_to_pledge)


def project():

    pledge_user_made = None
    able_to_pledge = True
    status_message = ""
    user_already_pledged_message = ""
    user_has_already_pledged =  False
    project_id = request.args(0)
    #Retrieve project
    project = db(db.project.id == project_id).select().first()

    #If project doesnt exist, redirect
    if project is None:
        redirect(URL('default','index'))

    #Set alert for owner of project
    if auth._get_user_id() == project.username:
        response.flash = DIV("You own this bootable", _class="alert alert-info")
        able_to_pledge = False

    #Redirect if project isnt available.
    if project.status == "Not Available":
        redirect(URL('default','index'))

    #If project is funded, set message
    elif project.status == "Funded":
        able_to_pledge = False
        status_message = DIV("This project has been funded and is now closed from pledges", _class="alert alert-success")

    #If project is not funded, set message
    elif project.status == "Not Funded":
        able_to_pledge = False
        status_message = DIV("This project has not been funded and is now closed from pledges", _class="alert alert-error")

    #Calculate percentage of goal completed. Also retrieve pledge levels on project and pledges made on project.
    percentage_completed = int((float(project.funding_raised)/float(project.funding_target))*100)
    pledge_levels = db(db.pledge_levels.project_id ==project_id).select(orderby=db.pledge_levels.pledge_amount)
    pledges_made_on_project = db((db.pledge_levels.project_id == project_id)  & (db.pledge_levels.id == db.pledges.pledge_levels_id)).select()

    #Finds out whether user has already pledged on a project
    for pledge in pledges_made_on_project:
        if pledge.pledges.username == auth._get_user_id():
            user_has_already_pledged = True
            pledge_user_made = pledge.pledges.pledge_levels_id
            user_already_pledged_message = DIV("You've already pledged on this project", _class="alert alert-info")


    return dict(project = project, percentage_completed = percentage_completed, pledge_levels = pledge_levels,
                pledges_made_on_project = pledges_made_on_project, user_has_already_pledged = user_has_already_pledged,
                able_to_pledge = able_to_pledge, status_message = status_message, pledge_user_made = pledge_user_made,
                user_already_pledged_message = user_already_pledged_message)



def make_pledge():

    user_has_already_pledged = False
    project_id = request.args(0)
    pledge_level_id = request.args(1)

    #If users isnt logged in, redirect to login with parameters to get back.
    if auth.is_logged_in() is False:
        redirect(URL('default','login', vars=dict(function = request.function,controller = request.controller, project_id = project_id, pledge_level_id = pledge_level_id )))

    pledges_made_on_project = db((db.pledge_levels.project_id == project_id)  & (db.pledge_levels.id == db.pledges.pledge_levels_id)).select()

    # Find out whether user has already pledge before
    for pledge in pledges_made_on_project:
        if pledge.pledges.username == auth._get_user_id():
            user_has_already_pledged = True
            previous_pledge_amount = pledge.pledge_levels.pledge_amount
            pledge_user_has_already_made = db(db.pledges.id == pledge.pledges.id).select().first()

            response.flash = DIV("You've already pledged on this project", _class="alert alert-info")

    form= FORM(BUTTON( I(_class="icon-shopping-cart icon-white"),' Yes, make the pledge', _type='submit', _class='btn btn-primary btn-large'))

    #Retreieve project and pledge level
    project = db(db.project.id == project_id).select().first()
    pledge_level = db(db.pledge_levels.id == pledge_level_id).select().first()

    if form.process().accepted:

        if user_has_already_pledged:

            #If user has already pledged, update records currently in database
            # Funding Raised needs to be recalculated.
            new_funding_raised = project.funding_raised - previous_pledge_amount + pledge_level.pledge_amount
            pledge_user_has_already_made.update_record(pledge_levels_id = pledge_level_id)
            project.update_record(funding_raised = new_funding_raised)
            session.flash = DIV( H2("Congratulations, You successfully pledged on this project"),_class="alert alert-success")
            redirect(URL('projects', 'project', args=project.id))

        else:
            #If users hasnt already pledged, add the neccessary rows
            db.pledges.insert(username = auth._get_user_id(), pledge_levels_id = pledge_level_id)
            new_funding_raised = project.funding_raised + pledge_level.pledge_amount
            project.update_record(funding_raised = new_funding_raised)
            session.flash = DIV( H2("Congratulations, You successfully pledged on this project"),_class="alert alert-success")
            redirect(URL('projects', 'project', args=project.id))



    return dict(project = project, pledge_level = pledge_level, form = form, user_has_already_pledged = user_has_already_pledged)

def search():

    #If category is specified, search that category
    if request.args(0) is not None:
        category =request.args(0).title()
        projects_returned_by_search = db((db.project.category==category) & (db.project.status != "Not Available")).select()

    else:
        #else search for a project by keyword specified
        category=None
        if request.vars.search:
            projects_returned_by_search = db(((db.project.title.like('%' + request.vars.search + '%'))| (db.project.short_description.like('%' +request.vars.search + '%'))) & (db.project.status != "Not Available")).select()

        else:
            #If no search terms specified, return all available projects.
            projects_returned_by_search = db(db.project.status != "Not Available").select()

    term_searched_for = request.vars.search

    return dict(projects_returned_by_search = projects_returned_by_search, term_searched_for = term_searched_for, category = category)

def explore_projects():

    return dict()