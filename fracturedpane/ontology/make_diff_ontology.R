#Procedure for translating parent child tables into binary differential ontologies

gene_df <- data.frame(parent = c("A","A","B","B","G","G","B","A","A","B","Q"),child = c("B","C","D","E","H","J","T","Blah","adsada","C","Z"))
gene_df <- gene_df[sample(1:dim(gene_df)[1]),]
gene_df <- gene_df[!duplicated(gene_df$child),]

feats=unique(unlist(gene_df))
gene_df <- rbind(data.frame(parent=0,child=feats[!feats%in%gene_df$child]),gene_df)

gene_df$childname <- ""
gene_df=gene_df[order(gene_df[,1]),]

prev=NULL
val="1"
for (ig in 1:dim(gene_df)[1]){
  val = c("1",paste0(val,"0"))[sum(gene_df$parent[ig]==prev)+1]
  prev = gene_df$parent[ig]
  #gene_df$childname[ig]=paste0(val)
  gene_df$childname[ig]=paste0(val,gene_df$childname[which(gene_df$child==gene_df$parent[ig])])
}

print(gene_df)

#Check uniqueness
print(length(unique(gene_df$childname))==dim(gene_df)[1])
