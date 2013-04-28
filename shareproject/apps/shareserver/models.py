"""
Data model objects for persistence to a relational database. In general these
will extend the AbstractEntityModel class below, but in some cases (e.g. SearchIndex)
the common fields are not needed and the model class will extend the base Django 
Model class. 
"""
from django.db import models
from django.db.models import fields


# This class defines common fields and behavior for all "entity" models, 
# such as Dog, Person, etc...
#
# Note: Explicitly specifying the blank and null keywords in some cases where they match defaults 
#       to make clear where fields will auto-populate or tolerate blank and/or null. 
#
class AbstractEntityModel(models.Model):
    # These fields will auto-populate themselves in child models, except for delete operations, of course
    created = fields.DateTimeField(auto_now_add=True, blank=True, null=False, db_index=True)
    last_modified = fields.DateTimeField(auto_now=True, blank=True, null=False, db_index=True)
    is_deleted = fields.BooleanField(default=False)
    # This will be needed when updating of Dog/Person fields is implemented, so the search terms can be synced
    search_index = models.ForeignKey('SearchIndex', null=True, db_index=True)
    
    # This field will need to be explicitly set before saving the child model, or it will be blank/null
    modified_by = models.ForeignKey('Person', blank=True, null=True, on_delete=models.SET_NULL, related_name="+")
    
    def create_index_for_search(self):
        # Child 
        term = self.get_search_term()
        # Don't proceed if the term is null
        if term is None:
            # If this is an update of an existing record that now has a null term, then delete the index
            if self.search_index is not None:
                self.search_index.delete()
            return
        
        if self.search_index is None:
            self.search_index = SearchIndex()
        self.search_index.term = term.lower()
        self.search_index.save()
    
    # Instead of adding a dependency to abc, seems simpler to raise a NotImplementedError
    def get_search_term(self):
        raise NotImplementedError("Concrete entity model classes must implement get_search_term")
       
    def save(self, *args, **kwargs):
        self.create_index_for_search()
        super(AbstractEntityModel, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True

# Defines an entity 'Dog' that belongs to a Person (many-to-one) and can have 0 or more 
# Pictures (one-to-many) via standard foreign key relationships. 
class Dog(AbstractEntityModel):
    name = fields.CharField(max_length=255, blank=False, null=False, db_index=False)  # allow empty dog names, this field will not be indexed
    owner = models.ForeignKey('Person', null=False, db_index=True)

    def get_search_term(self):
        return self.name

    def __unicode__(self):
        return '{{ "name": "{model.name}", "owner": {model.owner}, "created": {model.created}", "last_modified": "{model.last_modified}", "modified_by": {model.modified_by}, "is_deleted": {model.is_deleted} }}'.format(model=self);

# Defines an entity 'Person' that can have 0 or more Dogs (one-to-many)
class Person(AbstractEntityModel):
    first_name = fields.CharField(max_length=75, blank=True, null=True, db_index=False) # no reason to store repeated text for anonymous submissions
    middle_name = fields.CharField(max_length=75, blank=True, null=True, db_index=False)
    last_name = fields.CharField(max_length=100, blank=True, null=True, db_index=False)
    
    def get_search_term(self):
        term = ''
        if self.first_name is not None:
            term += self.first_name + ' '
        if self.middle_name is not None:
            term += self.middle_name + ' '
        if self.last_name is not None:
            term += self.last_name
        return term
    
    def __unicode__(self):
        return '{{ "first_name": "{model.first_name}", "middle_name": "{model.middle_name}", "last_name": "{model.last_name}", "created": {model.created}", "last_modified": "{model.last_modified}", "modified_by": {model.modified_by}, "is_deleted": {model.is_deleted} }}'.format(model=self);

# Defines an entity 'Picture' that belongs to a Dog (many-to-one)
class Picture(AbstractEntityModel):
    dog = models.ForeignKey('Dog', null=False, db_index=True)
    image = models.FileField(upload_to='originals')
    #thumbnail = easy_thumbnails.fields.ThumbnailerImageField()
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    score = fields.PositiveIntegerField(blank=True, null=False, db_index=True)
    
    
    def save(self, *args, **kwargs):
        if self.score is None:
            self.score = 0
        super(Picture, self).save(*args, **kwargs)
    
    # In this version, pictures do not have their own search terms, 
    # but it may be useful to add a caption in a later version
    def get_search_term(self):
        return None

# Defines a simple Django model that facilitates efficient case insensitive search in any relational database
class SearchIndex(models.Model):
    term = models.CharField(max_length=255)
    
# Defines a map between SearchIndex and Picture 
class SearchIndexPicture(models.Model):
    search_index = models.ForeignKey('SearchIndex', null=False, db_index=True)
    picture = models.ForeignKey('Picture', null=False, db_index=True)    

