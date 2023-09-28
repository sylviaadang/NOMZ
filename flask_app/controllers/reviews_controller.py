from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.reviews_model import Review
from flask_app.models.users_model import User


@app.route('/reviews/new')
def show_form():

    if 'user_id' not in session:
        return redirect('/register')

    return render_template('review.html')


@app.route('/reviews/create/<int:restaurant_id>', methods=['POST'])
def submit_new_review(restaurant_id):

    if not Review.validate_review(request.form):
        return redirect('/reviews/new')

    review_data = {
        ** request.form,
        'user_id' : session['user_id'],
        'restaurant_id' : restaurant_id
    }

    Review.create_review(review_data)

    return redirect('/')

# Show one review

@app.route('/reviews/<int:review_id>')
def show_review(review_id):

    if 'user_id' not in session:
        return redirect('/register')

    one_review = Review.get_one_review({'review_id' : review_id})
    one_user = User.getUserById({'user_id' : session['user_id']})

    return render_template('single_review.html', one_review=one_review, one_user=one_user)


#show edit form
@app.route('/reviews/edit/<int:review_id>')
def show_edit_form(review_id):

    if 'user_id' not in session:
        return redirect('/register')

    one_review = Review.get_one_review({'review_id' : review_id})

    return render_template('edit_review.html', one_review=one_review)

# submission route
@app.route('/reviews/update/<int:review_id>', methods=['POST'])
def submit_edit_form(review_id):

    if not Review.validate_review(request.form):
        return redirect(f'/reviews/edit/{review_id}')

    Review.update_review({
        'stars' : request.form['stars'],
        'comment' : request.form['comment'],
        'review_id' : review_id
    })

    return redirect('/')

# delete route

@app.route('/reviews/delete/<int:review_id>')
def delete_review(review_id):

    Review.delete_review({'review_id' : review_id})
    return redirect('/')
