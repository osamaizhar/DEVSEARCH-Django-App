from django.db import models
import uuid
from users.models import Profile
# Create your models here.

class Project(models.Model):
    owner=  models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL) # setting null to true here so we can run migration without data, SET_NULL is used so that we if someone deletes project accidently it can be retrived back
    title= models.CharField(max_length=200)
    description= models.TextField(null=True,blank=True)
    featured_image= models.ImageField(null=True,blank=True,default="default.jpg") # requires pillow to use
    demo_link= models.CharField(max_length=2000,null=True,blank=True)
    source_link= models.CharField(max_length=2000,null=True,blank=True)
    tags= models.ManyToManyField("Tag", blank=True) # using Tag as string since it is referenced afterwards so python will be able to find it
    vote_total= models.IntegerField(default=0,null=True,blank=True)
    vote_ratio= models.IntegerField(default=0,null=True,blank=True)
    created= models.DateTimeField(auto_now_add=True) # auto_now_add adds timestamp automatically as model instance is created
    id= models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False) # UUID 16 character unique ids
                                    # uuid4 is encoding type              # so no one can edit it
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio',"-vote_total"]  # ordering entries based on created field by default in ascending order

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id',flat=True) # look at notes for explaination , basically its supposed to give me all profiles who have reviewed
        return queryset

    @property # so that getVoteCount can be used in views, @property decorator allows you to define a method that can be accessed like an attribute, providing a cleaner way to implement read-only properties.
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
        
class Review(models.Model):
    VOTE_TYPE =(
        ('up',"Up Vote"), # first one is reference , second one is display output    
        ('down',"Down Vote")
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True) # CASCADE here will delete the review if profile is deleted
                                                    # if SET_NULL was used here then when project is delted this project field will be set to null 
                                                    # Cascade will delete all the reviews if the project is deletedf
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    body= models.TextField(null=True,blank=True)
    value= models.CharField(max_length=200, choices=VOTE_TYPE)
    created= models.DateTimeField(auto_now_add=True) # auto_now_add adds timestamp automatically as model instance is created
    id= models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    class Meta:
        unique_together= [['owner','project']] # this will make sure that no one can leave more than one review ,meaning we cannot have more than one owner for a project

    def __str__(self):
        return self.value

class Tag(models.Model):
    name= models.CharField(max_length=200)
    created= models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True,editable=False)

    def __str__(self):
        return self.name 