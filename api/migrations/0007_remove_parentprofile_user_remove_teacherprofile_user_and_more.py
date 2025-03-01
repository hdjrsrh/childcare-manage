# Generated by Django 5.1.5 on 2025-02-05 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_directorprofile_parentprofile_teacherprofile_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parentprofile",
            name="user",
        ),
        migrations.RemoveField(
            model_name="teacherprofile",
            name="user",
        ),
        migrations.AddField(
            model_name="customuser",
            name="adresse",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="child_age",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="child_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="diplome",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="documents",
            field=models.FileField(blank=True, null=True, upload_to="documents/"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="nom",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="nom_institution",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="num_tel",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="prenom",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="proof_of_identity",
            field=models.FileField(
                blank=True, null=True, upload_to="proof_of_identity/"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name="DirectorProfile",
        ),
        migrations.DeleteModel(
            name="ParentProfile",
        ),
        migrations.DeleteModel(
            name="TeacherProfile",
        ),
    ]
