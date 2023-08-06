import pandas as pd
from ovretl.loads_utils.calculate_single_load_total_quantities import (
    calculate_single_load_total_quantities,
    calculate_taxable_weight,
    calculate_weight_measurable,
)


def calculate_entity_loads(loads_df: pd.DataFrame, key: str):
    entity_loads = loads_df[~loads_df[key].isnull()]
    entity_loads = (
        entity_loads.groupby(key)
        .agg(
            total_number=pd.NamedAgg(column="total_number", aggfunc="sum"),
            total_volume=pd.NamedAgg(column="total_volume", aggfunc="sum"),
            total_weight=pd.NamedAgg(column="total_weight", aggfunc="sum"),
            hazardous=pd.NamedAgg(column="hazardous", aggfunc=lambda load_hazardous: load_hazardous.any()),
            lithium=pd.NamedAgg(column="lithium", aggfunc=lambda load_lithium: load_lithium.any()),
            refrigerated=pd.NamedAgg(column="refrigerated", aggfunc=lambda load_refrigerated: load_refrigerated.any()),
            magnetic=pd.NamedAgg(column="magnetic", aggfunc=lambda load_magnetic: load_magnetic.any()),
            non_stackable=pd.NamedAgg(
                column="non_stackable", aggfunc=lambda load_non_stackable: load_non_stackable.any()
            ),
        )
        .reset_index()
        .drop_duplicates(subset=[key])
    )
    entity_loads["weight_measurable"] = entity_loads.apply(
        lambda load: calculate_weight_measurable(load["total_weight"], load["total_volume"]), axis=1
    )
    entity_loads["taxable_weight"] = entity_loads.apply(
        lambda load: calculate_taxable_weight(load["total_weight"], load["total_volume"]), axis=1
    )
    return entity_loads


def calculate_shipments_propositions_loads(loads_df: pd.DataFrame):
    loads_df = loads_df.apply(calculate_single_load_total_quantities, axis=1)
    loads_df = loads_df.dropna(subset=["total_volume", "total_weight"])
    propositions_loads = calculate_entity_loads(loads_df=loads_df, key="proposition_id")
    shipments_loads = calculate_entity_loads(loads_df=loads_df, key="shipment_id")
    return pd.concat([propositions_loads, shipments_loads], sort=False)
