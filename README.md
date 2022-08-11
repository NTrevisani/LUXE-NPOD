# LUXE-NPOD

Repository with code for LUXE-NPOD studies

### Copy your plots on the web

General instructions:

    mkdir -p /etpwww/web/<your_login_name>/public_html/<your_web_directory>/

    cp -r e0ppw_3_0  /etpwww/web/<your_login_name>/public_html/<your_web_directory>/

    python gallery.py /etpwww/web/<your_login_name>/public_html/<your_web_directory>/e0ppw_3_0

One specific example:

    mkdir -p /etpwww/web/ntrevisa/public_html/2022_08_11/

    cp -r e0ppw_3_0  /etpwww/web/ntrevisa/public_html/2022_08_11/

    python gallery.py /etpwww/web/ntrevisa/public_html/2022_08_11/e0ppw_3_0/

Plots will be visible at:

    https://etpwww.etp.kit.edu/~<your_login_name>/<your_web_directory>/e0ppw_3_0/

In our example case:

    https://etpwww.etp.kit.edu/~ntrevisa/2022_08_11/e0ppw_3_0/