from flask import flash, request, render_template

from .models import Pet
from .config import app, db


db.create_all()
db.init_app(app)


def check_species(input_species):
    input_species = input_species.lower()
    allowed_species = ["dog", "cat"]
    if input_species not in allowed_species:
        raise Exception(
            {
                "Error": f"'{input_species}' species is not allowed. Allowed inputs include: {allowed_species} "
            }
        )


@app.route("/")
def index():
    """
    The index/home page route
    Returns index/home page
    """
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    """
    The submit page route
    Returns submit form
    Also handles POST requests from the submit form

    Raise an error if the species isn't in the allowed list
    """
    if request.method == "POST":
        # check for form data
        pet_name = request.form.get("name")
        pet_species = request.form.get("species")

        try:
            check_species(pet_species)
            new_pet = Pet(name=pet_name, species=pet_species)
            db.session.add(new_pet)
            db.session.commit()
            flash("pet submitted")
            # Issue: get a response object to return the newly created ID
            # Solution: Could just `query.all()` and return `.last()`, but I don't like that solution
        except Exception as e:
            flash(e)
            print("error", e)

    return render_template("submit.html")


@app.route("/retrieve", methods=["GET"])
def retrieve():
    """
    The retrieve page route
    Returns retrieval form
    Also handles GET requests based on search criteria

    Query all pets, then query for the searched-for-pet
    """
    all_pets = Pet.query.all()
    if request.args.get("id"):
        pet_id = request.args.get("id")
        pet = Pet.query.get(pet_id)
        flash(f"Pet ID: {pet.id} - Name: {pet.name}, a {pet.species}")
    return render_template("retrieve.html", pets=all_pets)


@app.route("/edit", methods=["GET", "POST", "PUT"])
def edit():
    """
    The edit page route
    Returns edit form

    Assuming a user knows a pet.id, they can edit that pet's data
    Get pet by ID then update its properties and commit
        But do not _add_ a new record
    Raise an error if the species isn't in the allowed list

    Notes:
    - I really don't like all the checking I'm doing on species here
    - I can't imagine how messy this would get if I had to check multiple columns
    - I usually lean on Django's built-in "choices" on the model
        -- but this isn't Django
    - I don't like the "None checking" I'm doing here. I would spend more time
        on organizing a happy path with try/except blocks and custom errors
    """
    if request.method == "POST" or request.method == "PUT":
        send_commit = True
        # this is actually just a PUT
        # but we're not _adding_ any records
        if request.form.get("id"):
            # get the pet to be edited
            pet_id = request.form.get("id")
            pet = Pet.query.get(pet_id)

            if pet is not None:
                if request.form.get("name") is not None:
                    pet.name = request.form.get("name")
                if request.form.get("species") is not None:
                    pet_species = request.form.get("species")

                try:
                    # NOTE: this restricts me to REQUIRING a pet species
                    # even though this should require species and/or name
                    check_species(pet_species)
                    pet.species = pet_species
                except Exception as e:
                    send_commit = False
                    flash(e)
                    print("error", e)
            else:
                flash("This ID does not exist")

            if send_commit:
                db.session.commit()
                flash(f"Pet Updated! ID: {pet.id} - Name: {pet.name}, a {pet.species}")
        else:
            flash("ID is required")
    all_pets = Pet.query.all()
    return render_template("edit.html", pets=all_pets)


@app.route("/delete", methods=["GET", "POST", "DELETE"])
def delete():
    """
    The delete page route
    Returns delete form

    Assuming a user knows a pet.id, they can delete a pet's record
    Get a pet record by ID, then remove it
    """
    if request.method == "POST" or request.method == "DELETE":
        # this is actually a DELETE
        # but we're not _adding_ any records
        if request.form.get("id"):
            # get the pet to be deleted
            pet_id = request.form.get("id")
            pet = Pet.query.get(pet_id)
            db.session.delete(pet)
            db.session.commit()

            flash(f"Pet Deleted!")
        else:
            flash("ID is required")
    all_pets = Pet.query.all()
    return render_template("delete.html", pets=all_pets)
