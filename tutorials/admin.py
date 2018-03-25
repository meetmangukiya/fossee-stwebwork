from django.contrib import admin

from .models import FOSS
from .models import Payment
from .models import TutorialDetail


models = [
    FOSS,
    Payment,
    TutorialDetail,
]

for model in models:
    admin.site.register(model)
