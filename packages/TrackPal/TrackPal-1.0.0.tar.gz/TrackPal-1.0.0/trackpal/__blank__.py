import pandas as pd
import trackpal as tp


trj_brownian = tp.simulate.brownian(n_tracks=10)
trj_linear = tp.simulate.brownian_linear(n_tracks=10)

trj_brownian["label"] = 0
trj_linear["label"] = 1

# concatenate and relabel
trj = tp.concat_relabel([trj_linear, trj_brownian])

# plot as lines
trj.groupby(trj.trackid).apply(
    tp.visu.plot_trj, coords=trj.coords, line_fmt=".-",
)

# prepare feature factory
feature_factory = tp.features.Features(frame=trj.frameid, coords=trj.coords)

# compute two features
conf_ratio = feature_factory.get("confinement_ratio")
speed_stats = feature_factory.get("speed_stats")

conf_ratio_res = trj.groupby(trj.trackid).apply(conf_ratio.compute)
speed_stats_res = trj.groupby(trj.trackid).apply(speed_stats.compute)

# retrieve labels assignment
y = trj.groupby(trj.trackid)["label"].first()

# merge into single DataFrame
features = pd.concat([conf_ratio_res, speed_stats_res, y], axis=1)

# plot with pandas
features.plot.scatter(
    x="confinement_ratio", y="speed_stats_mean", c="label", cmap="coolwarm"
)

