from django.shortcuts import render, redirect
from rest_framework import viewsets, mixins
from rest_framework import serializers


def organization_views(request):
    return render(request,'organization_table.html')


     
