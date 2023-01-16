import streamlit as st
import sys
import os
current_dir = os.path.dirname(__file__)
module_dir = os.path.join(current_dir,'fastapi')
sys.path.append(module_dir)

st.set_page_config(page_title='About The Legislative Record Tracker')
st.markdown("<h1 style='text-align: center; color: #007af9;'>About The Legislative Record Tracker</h1>", unsafe_allow_html=True)

# Add social media tags and links to the web page.
"""
[![Star](https://img.shields.io/badge/website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://www.hiruyhadgu.com/)
[![Follow](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/hiruy4hoco)
[![Follow](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/hiruy4hoco)

# Brief description of score parameters

"""

st.markdown("The Legislative Record Tracker gives  a summary/snapshot of the cumulative impact of\
    each Office Holders actions on the following issues: budget, affordable housing, school quality, accountability.")

st.markdown('**Budget**: too often, we do not know how a specific bill would affect the budget.\
     A seemingly innocuous bill could have some serious ramifications on a future budget.\
         Typically these are in the form of various land-use and zoning decisions.')

st.markdown("**Affordable Housing**: many politicians and developers like to use affordable\
     housing as a wedge issue instead of taking meaningful action to provide them. \
        Individual bill actions will be scored based on impact on affordable housing.")

st.markdown("**School quality**: indirect and direct impact on school quality due to\
     overcrowding, budget cuts, or zoning decisions will be scored.")

st.markdown("**Accountability**: lack of accountability in county government \
    leads to various undesirable outcomes. Any bill that impacts accountability is scored.")

st.markdown("Click on the 'Voting Record' to look at the office holders actions on the legislation.\
     A Council office holder could vote 'yes', 'no', 'abstain' or may not be present for the vote.")

st.markdown('The County Executive could "approve", "veto" a bill when taking action.\
     If a bill did not pass a stated position will be scored such as "support", "oppose". A "no action" will also be scored.')

st.markdown('Click on "Bill Detail" to learn more about each bill. The "Bill Number" on the "Voting Records" sheet is also\
     linked to each bill. Each bill is assigned a value of -2, -1, 1, or 2 depending on how it will impact the aforementioned \
        county issues: budget, affordable housing, school quality, and accountability.')

st.markdown('If no impact on the county issue, the cell is left blank.')

st.markdown('Sometimes, amendments to bills are also scored as they could enhance or dilute an original bill.')