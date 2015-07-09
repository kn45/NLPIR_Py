#!/bin/bash

term_cntnt_tb=kn45_chi2_cntnt
term_seg_tb=kn45_chi2_segs_uni

# seg_dir is the dir that contains the module folder nlpir_py 
seg_dir=/data0/result/chenting5/segmentation/NLPIR

function term_segment()
{
hive -e "
add file example.py;
add file $seg_dir/nlpir_py;
add file $seg_dir/usr_dict;

set hive.input.format=org.apache.hadoop.hive.ql.io.HiveInputFormat;
set mapred.map.tasks = 2000;

create table if not exists $term_seg_tb
(
	cat_id string,
	segs string
)
row format delimited fields terminated by '\t';

insert overwrite table $term_seg_tb
select distinct cat_id, segs from
(
	select transform(cat_id, content)
	using 'example.py c' as (cat_id, segs)
	from $term_cntnt_tb
)a;
"
}
term_segment

