import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt

fname = 'NOR_adm_shp/NOR_adm1.shp'

adm1_shapes = list(shpreader.Reader(fname).geometries())

ax = plt.axes(projection=ccrs.PlateCarree())

plt.title('Enkelt kart over Norge /m fylker')

#ax.coastlines(resolution='10m')
#ax.add_feature(cartopy.feature.LAND)
#ax.add_feature(cartopy.feature.OCEAN)
#ax.add_feature(cartopy.feature.COASTLINE)
#ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
#ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
ax.add_feature(cartopy.feature.RIVERS)

ax.add_geometries(adm1_shapes, ccrs.PlateCarree(),
                  edgecolor='black', facecolor='green', alpha=0.5)

ax.set_extent([3.3, 32, 57, 72], ccrs.PlateCarree())

# plotting
svg_lon, svg_lat = 5.7331, 58.97
bgo_lon, bgo_lat = 5.3221, 60.3913
osl_lon, osl_lat = 10.7522, 59.9139

plt.plot([svg_lon, bgo_lon, osl_lon], [svg_lat, bgo_lat, osl_lat],
         markersize=12,
         color='magenta', linewidth=0, marker='o',
         transform=ccrs.PlateCarree(),
         )

plt.text(svg_lon, svg_lat, 'Stavanger',
        fontsize=18,
        verticalalignment='center',
        horizontalalignment='right',
        transform=ccrs.PlateCarree())

plt.text(bgo_lon, bgo_lat, 'Bergen',
        fontsize=18,
        verticalalignment='center',
        horizontalalignment='right',
        transform=ccrs.PlateCarree())

plt.text(osl_lon, osl_lat, 'Oslo',
        fontsize=12,
        verticalalignment='center',
        horizontalalignment='right',
        transform=ccrs.PlateCarree())

plt.show()