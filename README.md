<img width="254" height="35" alt="powered-by-space-track" src="https://github.com/user-attachments/assets/7f3651bf-ae6b-4629-a537-a770357da416" />
<svg xmlns="http://www.w3.org/2000/svg" width="254.2528" height="35" viewBox="0 0 254.2528 35"><rect width="114.112" height="35" fill="#011892" /><rect x="114.112" width="140.1408" height="35" fill="#001caf" /><text x="57.056" y="17.5" dy="0.35em" font-size="12" font-family="Roboto, sans-serif" fill="#FFFFFF" text-anchor="middle" letter-spacing="2" font-weight="600" fill-opacity="1" </svg>

# Read Me

This is the source code for a research project I did with Dr. Denny Oliveira in the summer of 2025. Though the official project has long since ended, I still come in and update this occasionally. This code doesn't come together cohesively, it's more a collection of tools I built to download, manipulate, and display data from [space-track](https://www.space-track.org/auth/login).

The goal of our project was to explore the effects of geomagnetic activity (space weather) on the orbital drag of Starlink satellites. This included downloading and parsing over 1000 TLEs using space-track's REST API and building representative graphs (using matplotlib) with the data. I also pulled in Dst data from the [World Data Center at Kyoto University](https://wdc.kugi.kyoto-u.ac.jp/wdc/Sec3.html) and satellite weight information from [Dr. Jonathan McDowell's Space Report](https://planet4589.org/space/con/star/stats.html). (His website is an absolute treasure trove!)

Though a final paper was written, it will unfortunately not be submitted for publication due to poor planning and low prioritization. :(
