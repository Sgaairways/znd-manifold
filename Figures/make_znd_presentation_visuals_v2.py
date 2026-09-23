#!/usr/bin/env python3
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/"results"; OUT=ROOT/"presentation_figures"; OUT.mkdir(exist_ok=True)
VAL=RESULTS/"bilinear_multipoint_validation.csv"
SUM=RESULTS/"bilinear_multipoint_summary.csv"

TGRID=np.arange(300.,1001.,100.)
PGRID=np.arange(.1,5.01,.1)
MISSING=(400.,3.9)
STATES=[(351.5,.84),(351.5,2.54),(351.5,4.64),
        (651.5,.84),(651.5,2.54),(651.5,4.64),
        (951.5,.84),(951.5,2.54),(951.5,4.64)]
JAX=np.array([8.018,8.679,8.452,8.533,8.471,8.536,8.248,16.963,8.548])
SCIPY=np.array([39.900,40.120,39.655,39.679,40.036,39.600,40.881,43.425,40.561])

def save(fig,name):
    fig.savefig(OUT/f"{name}.png",dpi=300,bbox_inches="tight")
    plt.close(fig)

def clean(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

def col(df,*terms):
    for c in df.columns:
        s=str(c).lower()
        if all(t.lower() in s for t in terms): return c
    return None

def qlabel(q):
    return {"Temperature":"Temperature","Pressure":"Pressure","Y_H2":r"$H_2$",
    "Y_O2":r"$O_2$","Y_H2O":r"$H_2O$","Y_OH":"OH","Y_H":"H","Y_O":"O",
    "Y_HO2":r"$HO_2$","Y_H2O2":r"$H_2O_2$","Y_N2":r"$N_2$"}.get(q,q)

def manifold():
    pts=np.array([(T,P) for T in TGRID for P in PGRID
                  if not(np.isclose(T,400) and np.isclose(P,3.9))])
    v=np.array(STATES)
    fig,ax=plt.subplots(figsize=(10.5,6.2))
    ax.scatter(pts[:,0],pts[:,1],s=12,alpha=.55,label="Precomputed manifold state")
    ax.scatter(v[:,0],v[:,1],s=110,marker="*",zorder=4,label="Off-grid validation state")
    ax.scatter([400],[3.9],s=90,marker="x",linewidths=2.2,zorder=5,label="Timed-out state")
    ax.set(title="Precomputed ZND manifold and independent validation states",
           xlabel=r"Initial temperature, $T_1$ [K]",ylabel=r"Initial pressure, $P_1$ [atm]")
    ax.text(.02,.97,"399 generated manifold states\n9 off-grid validation states",
            transform=ax.transAxes,va="top",fontsize=11)
    ax.legend(frameon=False); clean(ax); fig.tight_layout(); save(fig,"01_manifold_validation_map")

def geometry():
    corners=np.array([[300,.8],[400,.8],[300,.9],[400,.9]])
    weights=[.291,.309,.194,.206]
    fig,ax=plt.subplots(figsize=(9.5,6.2))
    ax.scatter(corners[:,0],corners[:,1],s=150,label="Manifold corners")
    ax.scatter([351.5],[.84],s=190,marker="*",zorder=5,label="Query: 351.5 K, 0.84 atm")
    ax.plot([300,400,400,300,300],[.8,.8,.9,.9,.8],lw=1.5)
    ax.annotate("Nearest neighbor",xy=(400,.8),xytext=(365,.817),
                arrowprops=dict(arrowstyle="->",lw=1.5))
    for (T,P),w in zip(corners,weights): ax.text(T-13,P+.006,f"w={w:.3f}",fontsize=10)
    ax.set(title="How the off-grid ZND profile is reconstructed",
           xlabel=r"Initial temperature, $T_1$ [K]",ylabel=r"Initial pressure, $P_1$ [atm]",
           xlim=(280,420),ylim=(.775,.925))
    ax.legend(frameon=False,loc="lower left"); clean(ax); fig.tight_layout(); save(fig,"02_interpolation_geometry")


def nearest_vs_bilinear():
    # Original off-grid comparison at T1 = 351.5 K, P1 = 0.84 atm.
    # NRMSE values from the established nearest-neighbor and bilinear baselines.
    quantities = ["Temperature","Pressure",r"$H_2$",r"$O_2$",r"$H_2O$",
                  "OH","H","O",r"$HO_2$",r"$H_2O_2$"]
    nearest = np.array([0.861894,26.9835,0.907237,0.816316,1.43596,
                        4.19620,2.21621,3.06890,1.23382,1.32666])
    bilinear = np.array([0.0508568,3.45482,0.135000,0.121611,0.113180,
                         0.153022,0.309370,0.234949,0.144447,0.310320])

    # Sort by nearest-neighbor error so the comparison reads cleanly.
    order = np.argsort(nearest)
    quantities = [quantities[i] for i in order]
    nearest = nearest[order]
    bilinear = bilinear[order]

    y = np.arange(len(quantities))
    h = 0.36

    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.barh(y + h/2, nearest, height=h, label="Nearest neighbor")
    ax.barh(y - h/2, bilinear, height=h, label="Bilinear")

    ax.set_yticks(y, quantities)
    ax.set_xlabel("Profile NRMSE [%]")
    ax.set_title("Nearest neighbor vs bilinear reconstruction error\n"
                 r"Off-grid query: $T_1=351.5$ K, $P_1=0.84$ atm")
    ax.legend(frameon=False)

    # Pressure is much larger than the other quantities; use log scale so
    # both the large pressure error and smaller species errors remain visible.
    ax.set_xscale("log")
    ax.set_xlim(0.03, 40)
    ax.grid(axis="x", which="both", alpha=0.18)

    ax.text(0.98, 0.05,
            "Bilinear reduces NRMSE for every nonzero-error profile",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10)

    clean(ax)
    fig.tight_layout()
    save(fig, "03_nearest_vs_bilinear_nrmse")

def validation_df():
    if not VAL.exists(): raise FileNotFoundError(f"Missing {VAL}")
    return pd.read_csv(VAL)

def heatmap(df,q,name):
    qc=col(df,"quantity"); ec=col(df,"nrmse")
    sub=df[df[qc].astype(str)==q].copy()
    tc=col(sub,"t_k") or col(sub,"temperature")
    pc=col(sub,"p_atm") or col(sub,"pressure")
    cc=col(sub,"case")
    if tc is None or pc is None:
        if cc is not None:
            mp={i+1:s for i,s in enumerate(STATES)}
            sub["_T"]=[mp[int(x)][0] for x in sub[cc]]
            sub["_P"]=[mp[int(x)][1] for x in sub[cc]]
        elif len(sub)==9:
            sub["_T"]=[s[0] for s in STATES]; sub["_P"]=[s[1] for s in STATES]
        else: raise ValueError("Cannot recover validation T/P coordinates.")
        tc,pc="_T","_P"
    temps=[351.5,651.5,951.5]; press=[.84,2.54,4.64]; Z=np.full((3,3),np.nan)
    for i,T in enumerate(temps):
        for j,P in enumerate(press):
            r=sub[np.isclose(sub[tc].astype(float),T)&np.isclose(sub[pc].astype(float),P)]
            if len(r): Z[i,j]=float(r.iloc[0][ec])
    fig,ax=plt.subplots(figsize=(7.5,5.7)); im=ax.imshow(Z,origin="lower",aspect="auto")
    ax.set_xticks(range(3),[f"{p:.2f}" for p in press]); ax.set_yticks(range(3),[f"{t:.1f}" for t in temps])
    ax.set(xlabel=r"Initial pressure, $P_1$ [atm]",ylabel=r"Initial temperature, $T_1$ [K]",
           title=f"{qlabel(q)} profile interpolation error")
    for i in range(3):
        for j in range(3): ax.text(j,i,f"{Z[i,j]:.3f}%",ha="center",va="center",weight="bold")
    cb=fig.colorbar(im,ax=ax); cb.set_label("NRMSE [%]"); fig.tight_layout(); save(fig,name)

def aggregate():
    if not SUM.exists(): raise FileNotFoundError(f"Missing {SUM}")
    d=pd.read_csv(SUM); qc=col(d,"quantity"); mc=col(d,"mean","nrmse"); xc=col(d,"max","nrmse")
    d=d[d[qc].astype(str)!="Y_N2"].sort_values(mc)
    y=np.arange(len(d)); fig,ax=plt.subplots(figsize=(9.5,6.4))
    ax.barh(y,d[mc].astype(float),alpha=.75,label="Mean NRMSE")
    ax.scatter(d[xc].astype(float),y,s=65,marker="D",zorder=4,label="Maximum NRMSE")
    ax.set_yticks(y,[qlabel(q) for q in d[qc]])
    ax.set(xlabel="NRMSE [%]",title="Bilinear reconstruction accuracy across 9 off-grid states")
    ax.legend(frameon=False); clean(ax); fig.tight_layout(); save(fig,"07_aggregate_nrmse")

def speed():
    means=[SCIPY.mean(),JAX.mean()]; std=[SCIPY.std(ddof=1),JAX.std(ddof=1)]
    fig,ax=plt.subplots(figsize=(7.5,5.8)); bars=ax.bar(["SciPy","JAX"],means,yerr=std,capsize=6)
    ax.set(ylabel="Warmed lookup time [μs/query]",title="Warmed interpolation-only lookup on new MacBook Pro")
    for b,v in zip(bars,means): ax.text(b.get_x()+b.get_width()/2,v+1,f"{v:.2f} μs",ha="center",weight="bold")
    ax.text(.98,.92,f"Measured mean speedup: {SCIPY.mean()/JAX.mean():.2f}×",transform=ax.transAxes,ha="right")
    ax.text(.98,.84,"Case 8 timing spike included",transform=ax.transAxes,ha="right",fontsize=9)
    clean(ax); fig.tight_layout(); save(fig,"08_jax_scipy_speed_new_mbp")

def main():
    manifold(); geometry(); nearest_vs_bilinear(); d=validation_df()
    heatmap(d,"Temperature","04_validation_heatmap_temperature")
    heatmap(d,"Pressure","05_validation_heatmap_pressure")
    heatmap(d,"Y_HO2","06_validation_heatmap_HO2")
    aggregate(); speed()
    print(f"Done. PNG + SVG figures saved to {OUT}")

if __name__=="__main__": main()
