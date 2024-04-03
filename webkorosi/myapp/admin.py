from django.contrib import admin
from .models import Compounds

@admin.register(Compounds)

# Register your models here.
class compoundsAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'ref', 'IUPAC_name', 'CAS_number',
                    'formula','C','H','N','O','S','P',
                    'canocical_smile', 'InchI', 'molecular_weight', 'pKa', 'logP',
                    'logS', 'polar_surface_area', 'polarizability', 'hydrogen_acceptor',
                    'hydrogen_donor', 'HOMO_1', 'HOMO', 'LUMO', 'ionization_energy', 'electron_affinity',
                    'electronegativity', 'hardness', 'electrophilicity', 'delta_NFe', 'IE_EXP',
                    )