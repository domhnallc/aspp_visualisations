import matplotlib.pyplot as plt
import pandas as pd
import scipy
import jinja2
import tomli
import seaborn as sns



def get_dataframe(file, sort_key) -> pd.DataFrame:
    df_all_data = pd.read_csv(file, header=0, index_col=sort_key)

    return df_all_data


def filter_dataframe(df_in: pd.DataFrame) -> pd.DataFrame:
    filtered_df = df_in[
        [
            "ris_software_enum",
            "metadataFormat",
            "contains_software_set",
            "Manual_Num_sw_records",
            "Category",
            "RSE_group"
        ]
    ]
    return filtered_df


def vis_unis_with_sware(df_base):
    vals = df_base.groupby("Category").size()
    explode = [0.2, 0, 0]
    labels = [
        "Contains software",
        "Does not\ncontain software",
        "No direct software\n search capability",
    ]
    plt.pie(vals, labels=labels, autopct="%1.1f%%", explode=explode)
    plt.title("Software contained in \nUK Academic Institutional Repositories")
    plt.axis("equal")
    plt.savefig("./insts_category.pdf")
    print("Saved ./insts_category.pdf")
    # plt.show()


def vis_contains_sware_by_ris_type(df_base):
    cross_tab_prop = pd.crosstab(
        index=df_base["ris_software_enum"],
        columns=df_base["Category"],
        normalize="index",
    ).sort_values("Contains software")

    counts = df_base.groupby(['ris_software_enum']).size()
    print("\n\nCOUNTS PER RIS TYPE\n",counts, "\n\n\n")

    print(cross_tab_prop.to_latex())
    print(cross_tab_prop)

    cross_tab_prop.plot(kind="barh", stacked=True)
    plt.title(
        "Proportion of repositories that (a) contain software records,\n (b) contain no software records but "
        "are capable, \n(c) not capable of storing software records."
    )
    plt.ylabel("Repository framework software")
    plt.xlabel("Proportion of repositories")
    plt.show()
    chisq(cross_tab_prop=cross_tab_prop, subhead="Software records by RIS framework")


def vis_metdata_format_by_contains_sware(df_base):
    cross_tab_prop = pd.crosstab(
        index=df_base["metadataFormat"], columns=df_base["Category"], normalize="index"
    ).sort_values("Contains software")
    print(cross_tab_prop)

    print(cross_tab_prop.to_latex())
    counts = df_base.groupby(['metadataFormat']).size()
    print("\n\nCOUNTS PER METADATA TYPE\n",counts, "\n\n\n")
    cross_tab_prop.plot(kind="barh", stacked=True)
    plt.title(
        "Proportion of repositories that (a) contain software records,\n (b) contain no software records but "
        "are capable, \n(c) not capable of storing software records by metadata format."
    )
    plt.ylabel("Metadata format")
    plt.xlabel("Proportion of repositories")
    plt.show()

    chisq(cross_tab_prop=cross_tab_prop, subhead="Software records by metadata format")


def chisq(subhead, cross_tab_prop):
    print(
        "******************************************************\nChi-square test of independence"
    )
    print(subhead + "\n******************************************************")
    c, p, dof, expected = scipy.stats.chi2_contingency(cross_tab_prop)
    print("chi2=", c)
    print("p=", p)
    print("dof=", dof)
    print("expected=\n", expected)


def vis_unis_with_sware_barchart(df_filtered):
    df_sware_unis = df_filtered.sort_values(by=['Manual_Num_sw_records']).query("Manual_Num_sw_records >0")
    print(df_sware_unis)
    df_sware_unis.plot(kind="barh")
    plt.title("Number of software records >0 per institution")
    plt.xlabel("Software records")
    plt.grid(which="major", linestyle="-", linewidth="0.5", color="black")
    plt.grid(which="minor", linestyle=":", linewidth="0.5", color="black")
    plt.minorticks_on
    plt.savefig("./sware_recs_per_inst.pdf")
    plt.show()


def vis_russell_group_correlation(df_russell):

    print(df_russell.sort_values("uni_sld"))

    russell_cross_tab_prop = pd.crosstab(
        index=df_russell["Russell_member"],
        columns=df_russell["Category"],
        normalize="index",
    ).sort_values("Contains software")

    print(russell_cross_tab_prop)
    print(russell_cross_tab_prop.to_latex())
    russell_cross_tab_prop.plot(kind="barh", stacked=True)
    plt.title("Crosstabulation of membership of Russell group with software records in repository.")
    plt.show()

    counts = df_russell.groupby(['Russell_member']).size()
    print("\n\nCOUNTS PER MEMBERSHIP\n",counts, "\n\n\n")

    return russell_cross_tab_prop

def get_df_from_toml(file_path: str) -> pd.DataFrame:
    
    with open(file_path, "rb") as toml_file:
        data = tomli.load(toml_file)
    
    #print(data)

    df_groups = pd.DataFrame.from_dict(data, orient='index')

    #print(df_groups)

    return df_groups

def correlate_sware_rse_groups(df: pd.DataFrame):

    cross_tab_prop = pd.crosstab(
        index=df["RSE_group"],
        columns=df["Category"],
        normalize="index",
    ).sort_values("RSE_group")
    print(cross_tab_prop)
    print(cross_tab_prop.to_latex())


    return cross_tab_prop

def vis_crosstab_heatmap(crosstab: pd.crosstab, title: str):

    plt.figure(figsize=(12,12))
    plt.title(title)
    sns.heatmap(crosstab, cmap='crest')
    plt.show()

def vis_cumulative_sware_recs(df_filtered):
    df_sware_unis = df_filtered.sort_values(by=['Manual_Num_sw_records'], ascending=[False]).query("Manual_Num_sw_records >0")
    df_sware_unis['cumul_percent'] = 100 * (df_sware_unis['Manual_Num_sw_records'].cumsum()/df_sware_unis['Manual_Num_sw_records'].sum()) 
    df_sware_unis.reset_index(drop=True, inplace=True)
    print(df_sware_unis['cumul_percent'])
    df_sware_unis['cumul_percent'].plot(kind="line")
    plt.grid(which="major", linestyle="-", linewidth="0.5", color="black")
    plt.grid(which="minor", linestyle=":", linewidth="0.5", color="black")
    plt.minorticks_on
    plt.xlabel("Rank number of institutes in order of quantity of software (high-low)")
    plt.ylabel("Cumulative percentage of all software records")
    plt.show()

    
def main():
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    data_file = "./complete_dataset_manual_adjustment.csv"
    # load and prep file
    df_all_data = get_dataframe(data_file, sort_key='name')
    df_filtered = filter_dataframe(df_all_data)
    '''
    # produce cumulutative curve of 
    vis_cumulative_sware_recs(df_filtered)
    vis_unis_with_sware(df_filtered)
    
    # vis software by RIS type
    vis_contains_sware_by_ris_type(df_filtered)

    # vis software by metadata format
    vis_metdata_format_by_contains_sware(df_filtered)
    '''

    # bar chart of unis with software only
    vis_unis_with_sware_barchart(df_filtered)

    # Correlate Russell Group members with s'ware
    df_russell = get_dataframe("./russell_sld_sware.csv", sort_key="uni_sld")
    russell_top_20_sw = df_russell.sort_values("Manual_Num_sw_records", ascending=False).head(20)
    print("\n\nTop 20 Universities in order of number of software records in repository, and membership of Russell Group\n\n",russell_top_20_sw)
    russell_ctp = vis_russell_group_correlation(df_russell)
    chisq(subhead="Membership of Russell Group vs Software in repository", cross_tab_prop=russell_ctp)
    vis_crosstab_heatmap(russell_ctp, "Heatmap of cross tabulation between Russell Group Membership and software records in repository.")
'''
    # Correlate RSE groups with s'ware
    print(df_filtered.keys())
    df_rse_groups = df_filtered[['RSE_group','Category']]
    groups_cross_tab = correlate_sware_rse_groups(df_rse_groups)
    chisq(cross_tab_prop=groups_cross_tab, subhead="RSE Groups vs sware records")
    vis_crosstab_heatmap(groups_cross_tab, "Heatmap of cross tabulation between RSE Group present in Institute and sofware records in repository.")
'''
main()

