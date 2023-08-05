Neuroharmony: A tool for harmonizing volumetric MRI data from unseen scanners
=============================================================================

The model presented in `Garcia-Dias, et
al. (2020) <https://www.sciencedirect.com/science/article/pii/S1053811920306133>`__.

Documentation
-------------

`neuroharmony.readthedocs.io <https://neuroharmony.readthedocs.io>`__


Install Neuroharmony.
---------------------

::

   pip install neuroharmony

Example of use:
===============

Pre-trained Neuroharmony model
------------------------------

An example plot of how to load and apply pre-trained a Neuroharmony
model.

.. code:: python

   import matplotlib.pyplot as plt
   from neuroharmony.models.harmonization import fetch_trained_model, fetch_sample
   import seaborn as sns

   X = fetch_sample()
   neuroharmony = fetch_trained_model()
   x_harmonized = neuroharmony.transform(X)

   rois = ['Left-Hippocampus',
           'lh_bankssts_volume',
           'lh_posteriorcingulate_volume',
           'lh_superiorfrontal_volume',
           'rh_frontalpole_volume',
           'rh_parsopercularis_volume',
           'rh_parstriangularis_volume',
           'rh_superiorfrontal_volume',
           'Right-Cerebellum-White-Matter',
           ]
   fig, axes = plt.subplots(3, 3, figsize=(10, 10))
   for roi, ax in zip(rois, axes.flatten()):
       ax.plot(neuroharmony.kde_data_[roi]['x'], neuroharmony.kde_data_[roi]['y'],
               color='#fcb85b', ls='--', label='ComBat harmonized training set')
       sns.kdeplot(X[roi], color='#f47376', ls=':', legend=False, ax=ax, label='Original test set')
       sns.kdeplot(x_harmonized[roi], color='#00bcab', ls='-', legend=False, ax=ax, label='Harmonized test set')
       ax.set_xlabel(roi, fontsize=13)
   axes.flatten()[2].legend(ncol=3, bbox_to_anchor=(0.8, 1.175), fontsize=13)
   axes.flatten()[3].set_ylabel('Density', fontsize=15)
   plt.subplots_adjust(left=0.07, right=0.99,
                       bottom=0.05, top=0.96,
                       hspace=0.20, wspace=0.20)
   plt.savefig('test.png', dpi=200)
   plt.show()
