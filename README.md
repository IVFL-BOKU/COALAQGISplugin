# COALA QGIS plugin
The QGIS plugin for COALA API was  implemented in a final version by ARIESPACE srl. The plugin provides a quick download of a selection of COALA products using the COALA APIs and it allows the visualisation directly in QGIS. Available indicators are: NDVI, fcover, LAI, NDMI, STR, ET (Crop evapotranspiration [mm]) and CWR (Crop water requirements [mm]).  
 
The QGIS plugin can be downloaded from this repository. 

The instruction for installation and a dedicated QGIS guide was developed and it is available here:  

https://www.coalaproject.eu/coala-project/qgis-plugin-guide/ 

The figure below shows the from COALA QGIS plugin that can be used to access a selection for COALA indicators for a specific geometry.  

https://www.coalaproject.eu/wp-content/uploads/2023/06/5.jpg 

Figure 1 screen capture of the COALA QGIS Plug-in for downloading COALA indicators.  
 
After downloading the original raster data are available in the list of QGIS layers for local processing and futher integration in existing workflows as shown in the following figure:   

https://www.coalaproject.eu/wp-content/uploads/2023/06/qgis2.png 

Figure 2 Screen capture of the COALA QGIS plug-in in operation. Data are downloaded and available in the list of layers in QGIS.  

A test token can be used:  
6ca6988a12f5dceaf72ede6c07f12c94baf9b50497234bccc32099ab9c84cdf56a96246d8788e080 
 
For this token, the regions on interest within the Sentinel-2 tiles are activated: 
 
55HCA (Cobram, Australia) and 55HDC (Griffith, Australia)  
33UXP (Vienna, Austria and Bratislava, Slovakia) and 33UVP (Linz, Austria) 
 
for a period of 365 days (always from current date) with the availability of the following indicators: NDVI, fcover, LAI, NDMI, STR, ET, CWR (daily for the latest 50 days from current date), MZM and NNI 
