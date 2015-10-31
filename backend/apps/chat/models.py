from django.db import models

class Chat(models.Model):
    
    name_room = models.CharField(max_length=20)

    # class Meta:
    #     ordering = ("name_room",)
    #
    # def __unicode__(self):
    #     return self.name_room


class Message(models.Model):

    text_chat = models.CharField(max_length=400)
    user = models.ForeignKey('users.User')
    date_chat = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat)
    # avatar = models.ForeignKey('users.User')






