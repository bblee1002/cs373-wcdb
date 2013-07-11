<?xml version="1.0" ?>

<!-- World Crises XML using schema (WorldCrises.xsd) -->

<WorldCrises>
    <!-- Example Crisis element -->
    <Crisis ID="CRI_NRINFL" Name="2013 Northern India Floods">



        <Organizations>
            <Org ID="ORG_PMRLFD" />
        </Organizations>
        <Kind>Natural Disaster</Kind>
        <Date>2013-06-14</Date>
        <Time>09:00:00+05:30</Time>
        <Locations>
            <li>Uttarakhand, India</li>
            <li>Himachal Pradesh, India</li>
            <li>Nepal</li>
        </Locations>
        <HumanImpact>
            <li>More than 1000 dead.</li>
            <li>Over 70000 stranded.</li>
            <li>Over 100000 more evacuated.</li>
        </HumanImpact>
        <EconomicImpact>
            <li>Ongoing large-scale crisis, impact has not been evaluated as of July 5th 2013.</li>
            <li>Estimates over 500 Billion INR (10 Billion USD)</li>
        </EconomicImpact>
        <ResourcesNeeded>
            <li>Prime Minister of India undertook an aerial survey of the affected areas and announced 1,000 crore (US$170 million) aid package for disaster relief efforts in the state.</li>
            <li>The Indian Army and the National Disaster Response Force were deployed to evacuate stranded people on June 15th 2013.</li>
            <li>The Indian Airforce has flown hundreds of sorties every day to airdrop food and fuel for trapped villages.</li>
        </ResourcesNeeded>
        <WaysToHelp>
            <!-- Put text with optional hyperlinks here -->
            <li href="http://google.org/personfinder/2013-uttrakhand-floods/">Google Person Finder</li>
            <li href="https://pmnrf.gov.in/">Donate to Prime Minister's Relief Fund</li>
            <li>Like a page on Facebook</li>
        </WaysToHelp>
        <Common>
            <Citations>
                <!-- Put text with optional hyperlinks here -->
                <li>The Hindustan Times</li>
                <li>The Times of India</li>
            </Citations>
            <ExternalLinks>
                <!-- Put text with compulsory hyperlinks here -->
                <li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li>
            </ExternalLinks>
            
            <!-- hrefs optional in the following depending on how you want them to behave on your site -->
            <Images>
                <!-- Put full URLs to images here, display them on your site in your own cool way -->
                <li embed="http://images.jagran.com/ukhand-ss-02-07-13.jpg" text="This is the alt element of the image." />
                <li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" />
            </Images>
            <Videos>
                <!-- Put youtube link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by youtube) -->
                <!-- Embed example for your site: <iframe width="420" height="315" src="[THIS LINK]" frameborder="0" allowfullscreen></iframe> -->
                <li embed="//www.youtube.com/embed/qV3s7Sa6B6w" />
            </Videos>
            <Maps>
                <!-- Put google maps link here (pull this URL out of the src="[GET THIS LINK]" attribute in the embed object given by google maps) -->
                <!-- Embed example for your site: <iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="[THIS LINK]"></iframe> -->
                <li embed="https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed" />
            </Maps>
            <Feeds>
                <!-- Put feed URL here and embed on your site in your own cool way-->
                <li embed="[WHATEVER A FEED URL LOOKS LIKE]" />
            </Feeds>

            <!-- Optional summary field for extra random data -->
            <Summary>
              Lorem ipsum...
            </Summary>
        </Common>
    </Crisis>
    
    <!-- Example Person element -->
    <Person ID="PER_MNSNGH" Name="Manmohan Singh">
        <Crises>
            <Crisis ID="CRI_NRINFL" />
        </Crises>
        <Organizations>
            <Org ID="ORG_PMRLFD" />
        </Organizations>
        <Kind>Politician</Kind>
        <Location>India</Location>
        <!-- See Crisis element above for examples of everything under <Common> -->
    </Person>
    
    <!-- Example Organization element -->
    <Organization ID="ORG_PMRLFD" Name="Prime Minister's Relief Fund">
        <Crises>
            <Crisis ID="CRI_NRINFL" />
        </Crises>
        <People>
            <Person ID="PER_MNSNGH" />
        </People>
        <Kind>Governement Fund</Kind>
        <Location>India</Location>
        <History>
            <li>Founded in 1948.</li>
        </History>
        <ContactInfo>
            <li>Phone: (+91) 1-800-DONTKNOW</li>
            <li>Email: donot@email.me</li>
        </ContactInfo>
        <!-- See Crisis element above for examples of everything under <Common> -->
    </Organization>
</WorldCrises>
