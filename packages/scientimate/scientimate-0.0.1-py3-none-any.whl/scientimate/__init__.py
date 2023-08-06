"""
.. ++++++++++++++++++++++++++++++++YA LATIF++++++++++++++++++++++++++++++++++
.. +                                                                        +
.. + ScientiMate                                                            +
.. + Earth-Science Data Analysis Library                                    +
.. +                                                                        +
.. + Developed by: Arash Karimpour                                          +
.. + Contact     : www.arashkarimpour.com                                   +
.. + Developed/Updated (yyyy-mm-dd): 2020-02-01                             +
.. +                                                                        +
.. ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

#Import modules
#https://towardsdatascience.com/whats-init-for-me-d70a312da583
#Method 1
#    __init__.py
#        from .foo import *
#    Usage:
#        import example_pkg
#        example_pkg.foo_func()

#Method 2
#    __init__.py
#        from .foo import foo_func
#    Usage:
#        import example_pkg
#        example_pkg.foo_func()

#Method 3
#    __init__.py
#        import example_pkg.foo
#    Usage:
#        import example_pkg
#        example_pkg.foo.foo_func()

#    Usage:
#        from example_pkg import foo
#        foo.foo_func()

#    Usage:
#        import example_pkg.foo as ex_foo
#        ex_foo.foo_func()


#Colormap
#--------
# from .gencolormap import gencolormap
# from .seqcolormap import seqcolormap
# from .topocolormap import topocolormap

#Data Manipulating
#-----------------
from .downsamplex import downsamplex
# from .downsamplexy import downsamplexy
# from .downsamplexyz import downsamplexyz
# from .interpgrid2xyz import interpgrid2xyz
from .interpxyz2grid import interpxyz2grid
# from .interpxyz2xyz import interpxyz2xyz
# from .readdatafile import readdatafile
from .replacemissing1d import replacemissing1d
# from .replacemissing2d import replacemissing2d
from .replaceoutlier import replaceoutlier
# from .replacespike3dps import replacespike3dps
# from .replacespikediff import replacespikediff
# from .replacespikeenvelope import replacespikeenvelope
from .smoothsignal import smoothsignal

#Hurricane
#---------
# from .hurricanebackgroundwind import hurricanebackgroundwind
# from .hurricanedpcpt import hurricanedpcpt
# from .hurricanepressureh80 import hurricanepressureh80
# from .hurricanetranslationvel import hurricanetranslationvel
# from .hurricanewavecontourcem import hurricanewavecontourcem
# from .hurricanewavecontourh16 import hurricanewavecontourh16
# from .hurricanewavecontoury88 import hurricanewavecontoury88
# from .hurricanewavemax import hurricanewavemax
# from .hurricanewindh08 import hurricanewindh08
# from .hurricanewindh80 import hurricanewindh80
# from .hurricanewindinflowangle import hurricanewindinflowangle
# from .hurricanewindvel import hurricanewindvel
# from .hurricanewindvelmax import hurricanewindvelmax
# from .hurricanewindvelmaxh08 import hurricanewindvelmaxh08
# from .hurricanewindvelmaxh80 import hurricanewindvelmaxh80
# from .readnhchurricane import readnhchurricane
# from .stormsurge1d import stormsurge1d

#Mapping
#-------
# from .convertdir import convertdir
# from .distancecart import distancecart
# from .distancegc import distancegc
# from .endpointcart import endpointcart
# from .gridgenerator import gridgenerator
# from .intersectgc import intersectgc
# from .intersectlineedge import intersectlineedge
# from .pointscart import pointscart
# from .readxyz import readxyz
# from .reckongc import reckongc
# from .waypointsgc import waypointsgc
# from .windfetch import windfetch
# from .zprofilepath import zprofilepath

#OCEANLYZ
#--------
from .oceanlyz import oceanlyz
from .PcorFFTFun import PcorFFTFun
from .PcorZerocrossingFun import PcorZerocrossingFun
from .SeaSwellFun import SeaSwellFun
from .WaveSpectraFun import WaveSpectraFun
from .WaveZerocrossingFun import WaveZerocrossingFun

#Plotting
#--------
# from .plot2d import plot2d
# from .plot2dsubplot import plot2dsubplot
# from .plot2dtimeseries import plot2dtimeseries
# from .plot3d import plot3d
# from .plot3ddem import plot3ddem
# from .plot3dhillshades import plot3dhillshades
# from .plot3dtopo import plot3dtopo

#Signal Processing
#-----------------
# from .bartlettpsd import bartlettpsd
# from .fftfrequency import fftfrequency
# from .periodogrampsd import periodogrampsd
# from .psd2timeseries import psd2timeseries
# from .spectrogrampsd import spectrogrampsd
# from .welchpsd import welchpsd

#Statistics
#----------
# from .curvefit2d import curvefit2d
# from .curvefit3d import curvefit3d
# from .dataoverview import dataoverview
# from .findextremum import findextremum
# from .findknn import findknn
# from .fitgoodness import fitgoodness
# from .levelcrossing import levelcrossing
# from .probability1d import probability1d
# from .probability2d import probability2d
# from .similaritymeasure import similaritymeasure

#Swan
#----
# from .swandepthgrid import swandepthgrid
# from .swanvectorvarspconst import swanvectorvarspconst
# from .swanvectorvarspvariedgrid import swanvectorvarspvariedgrid
# from .swanvectorvarspvariedsct import swanvectorvarspvariedsct
# from .swanwaterlevelspconst import swanwaterlevelspconst
# from .swanwaterlevelspvariedgrid import swanwaterlevelspvariedgrid
# from .swanwaterlevelspvariedsct import swanwaterlevelspvariedsct
# from .swanwindspconst import swanwindspconst
# from .swanwindspvariedgrid import swanwindspvariedgrid
# from .swanwindspvariedsct import swanwindspvariedsct

#Water Wave Data Analysis
#------------------------
# from .diagnostictail import diagnostictail
# from .pressure2surfaceelevfft import pressure2surfaceelevfft
# from .pressure2surfaceelevzcross import pressure2surfaceelevzcross
# from .seaswell1d import seaswell1d
# from .velocity2surfaceelevfft import velocity2surfaceelevfft
# from .velocity2surfaceelevzcross import velocity2surfaceelevzcross
# from .wavefrompressurepsd import wavefrompressurepsd
# from .wavefrompressurezcross import wavefrompressurezcross
# from .wavefromsurfaceelevpsd import wavefromsurfaceelevpsd
# from .wavefromsurfaceelevzcross import wavefromsurfaceelevzcross
# from .wavefromvelocitypsd import wavefromvelocitypsd
# from .wavefromvelocityzcross import wavefromvelocityzcross
# from .wavepropfrompsd import wavepropfrompsd

#Water Wave Directional Analysis
#-------------------------------
# from .directionalpsd import directionalpsd
# from .directionalpsdetauv import directionalpsdetauv
# from .directionalpsdpuv import directionalpsdpuv
# from .enu2truenorth import enu2truenorth
# from .wavediretauv import wavediretauv
# from .wavedirpuv import wavedirpuv

#Water Wave Parametric Model
#---------------------------
# from .asymptlimit import asymptlimit
# from .equivfetchdeep import equivfetchdeep
# from .equivfetchshallow import equivfetchshallow
# from .fullydevwave import fullydevwave
# from .mindurationdeep import mindurationdeep
# from .mindurationshallow import mindurationshallow
# from .parametricwavedeep import parametricwavedeep
# from .parametricwaveshallow import parametricwaveshallow
# from .wavedim2dimless import wavedim2dimless
# from .wavedimless2dim import wavedimless2dim

#Water Wave Properties
#---------------------
# from .bretpsd import bretpsd
# from .donelanpsd import donelanpsd
# from .incidentreflectedwave import incidentreflectedwave
# from .jonswappsd import jonswappsd
# from .linearwavegenerator import linearwavegenerator
# from .linearwavesuperposition import linearwavesuperposition
# from .pmpsd import pmpsd
# from .pressureresponse import pressureresponse
# from .randomwavegenerator import randomwavegenerator
# from .stokeswavegenerator import stokeswavegenerator
# from .stokeswavesuperposition import stokeswavesuperposition
# from .tmapsd import tmapsd
# from .wavebedstress import wavebedstress
# from .wavedispersion import wavedispersion
# from .wavedispersionds import wavedispersionds
# from .waveorbitalvelocity import waveorbitalvelocity
# from .wavepower import wavepower
# from .wavepowerfrompsd import wavepowerfrompsd
# from .wavevel2wlconvfactor import wavevel2wlconvfactor

#Wind
#----
# from .directionavg import directionavg
# from .surfaceroughness import surfaceroughness
# from .sustainedwindduration import sustainedwindduration
# from .windavg import windavg
# from .winddrag import winddrag
# from .windgustfactor import windgustfactor
# from .windvelz1toz2 import windvelz1toz2


__version__ = "1.0.0"
__author__ = 'Arash Karimpour'
#__credits__ = 'xyz Laboratory'    
