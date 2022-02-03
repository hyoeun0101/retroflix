from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from movie.models import Movie
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from review.models import Review, age

# Create your views here.


## Form이 제 역할을 못하면 쓸 기능입니다.
# @login_required
# def review_create(request, movie_id):
    
#     movie = get_object_or_404(Movie, id=movie_id)
#     if request.method == 'POST':
#         content = request.POST.get('review-content')
#         star = request.POST.get('review-star')
#         Movie.objects.create(movie=movie, author=request.user, content=content, star=star).save()
#         movie.star = movie.reviews.all().aggregate(Avg('star')).get('star__avg')
#         movie.save()
#         return redirect('/main')


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    total_user = movie.reviews.all()
    total_user_count = total_user.count()
    male_user_count = total_user.filter(customuser__gender__ieaxct='male').count()

    # 리뷰 성별 비율
    male_gender_rate = (male_user_count/total_user_count) * 100
    female_gender_rate = 100 - male_gender_rate
    
    # 리뷰 연령별 비율  

    user_age = list(map(lambda x : age(x.author.birthday), total_user))
    gen_10 = gen_20 = gen_30 = gen_40 = 0
    
    for age in user_age:
        if age >= 40:
            gen_40 += 1
        elif age >= 30:
            gen_30 += 2
        elif age >= 20:
            gen_20 += 1
        else:
            gen_10 += 1       


    context = {
        'movie': movie,
        'male_gender_rate':male_gender_rate,
        'female_gender_rate': female_gender_rate,
        'generation_10_rate': '',
        'generation_20_rate': '',
        'generation_30_rate': '',
        'generation_40_rate': '',        
    }


@login_required
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            review.save()
            movie.star = movie.reviews.all().aggregate(Avg('star')).get('star__avg')
            movie.save()
            return redirect('main')
        
    else:
        form = ReviewForm()
        context = {'form':form}
        return render(request, 'review/review.html', context)


@login_required
def review_modify(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()            
            movie.star = movie.reviews.all().aggregate(Avg('star')).get('star__avg')
            movie.save()
            return redirect('main')
    else:
        form = ReviewForm(instance=movie)
        context = {'form':form}
        return render(request, 'review/review.html', context)
            

        
@login_required
def review_delete(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id = review_id)
        movie = get_object_or_404(Movie, id = review.movie.id)
        review.delete()
        movie.rate = movie.reviews.all().aggregate(Avg('star')).get('star__avg')
        movie.save()
        return redirect('/main')
