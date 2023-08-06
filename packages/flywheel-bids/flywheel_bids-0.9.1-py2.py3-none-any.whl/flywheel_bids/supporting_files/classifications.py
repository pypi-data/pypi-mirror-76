classifications = {
        'anat': {
            'T1w': {'Measurement': 'T1', 'Intent':'Structural'},
            'T2w': {'Measurement': 'T2', 'Intent':'Structural'},
            'T1rho': {'Custom': 'T1rho'},
            'T1map': {'Measurement': 'T1', 'Intent':'Structural', 'Features': 'Quantitative'},
            'T2map': {'Measurement': 'T2', 'Intent':'Structural', 'Features': 'Quantitative'},
            'T2star': {'Measurement': 'T2*', 'Intent':'Structural'},
            'FLAIR': {'Custom': 'FLAIR'},
            'FLASH': {'Custom': 'FLASH'},
            'PD': {'Measurement': 'PD', 'Intent':'Structural'},
            'PDmap': {'Custom': 'PD-Map'},
            'PDT2': {'Measurement': ['PD', 'T2'], 'Intent':'Structural'},
            'inplaneT1': {'Measurement': 'T1', 'Intent':'Structural', 'Features': 'In-Plane'},
            'inplaneT2': {'Measurement': 'T2', 'Intent':'Structural', 'Features': 'In-Plane'},
            'angio': {'Custom': 'Angio'},
            'defacemask': {'Custom': 'Defacemask'},
            'SWImagandphase': {'Custom': 'SWI'},
        },
        'func': {
            'bold': {'Intent': 'Functional'},
            'events': {'Intent': 'Functional'},
            'sbref': {'Intent': 'Functional'},
            'stim': {'Intent': 'Functional', 'Custom': 'Stim'},         # stimulus
            'physio': {'Intent': 'Functional', 'Custom': 'Physio'},     # physio
        },
        'beh' : {
            'events': {'Custom': 'Behavioral'},
            'stim': {'Custom': 'Stim'},    # stimulus
            'physio': {'Custom': 'Physio'}     # physio
        },
        'dwi' : {
            'dwi': {'Measurement': 'Diffusion', 'Intent':'Structural'},
            'sbref': {'Measurement': 'Diffusion', 'Intent':'Structural'}
        },
        'fmap': {
            'phasediff': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
            'magnitude1': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
            'magnitude2': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
            'phase1': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
            'phase2': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
            'magnitude': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
            'fieldmap': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
            'epi': {'Measurement': 'B0', 'Intent': 'Fieldmap'},
        }
    }

