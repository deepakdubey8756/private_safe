from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note
from datetime import datetime
from utilities import genpass, authValidation

# Create your tests here.

class NoteTest(TestCase):

    username = "test_deepak"
    user_email = "test_deepak@gmail.com"
    user_password = "test_deepak_pass"

    def setUp(self):
        print("Testing notes models")


    def test_create_user(self):
        user = User.objects.create_user(self.username, self.user_email, self.user_password)
        user.save()
        created_data = [user.username, user.email]
        self.assertEqual(created_data, [self.username, self.user_email])
        self.assertNotEqual(user.password, self.user_password)

    def test_create_notes(self):

        user = User.objects.create_user(self.username, self.user_email, self.user_password)

        name = "Instagram"
        username = "parvography"
        password = "ThisIsMyPass"

        note = Note.objects.create(author=user, name=name, username=username, password = password)

        now = datetime.now()

        self.assertEqual(str(note), name)

        self.assertEqual(note.username, username)

        self.assertEqual(note.password, password)
        
        note_creation_time = [
            note.date_modified.year,
            note.date_modified.month,
            note.date_modified.day,
            note.date_modified.hour, 
            ]
        current_time = [now.year,
                        now.month,
                        now.day,
                        now.hour, 
                        ]
        self.assertEqual(current_time, note_creation_time)


class TestUtilities(TestCase):

    def setUp(self):
        print("Testing differnt unitilities")


    def test_password_generation(self):
        checkPass = {}
        isOk = True
        for i in range(5):
            password = genpass.genpass()
            if password in checkPass:
                isOk = False
                break
            checkPass[password] = password
        

        self.assertEqual(isOk, True)
    
