#Procedure for translating parent child tables into binary differential ontologies

gene_df <- data.frame(parent = c("A","A","B","B","G","G","B","A","A","B","Q"),child = c("B","C","D","E","H","J","T","Blah","adsada","C","Z"))
gene_df <- gene_df[sample(1:dim(gene_df)[1]),]
#gene_df <- gene_df[!duplicated(gene_df$child),]

feats=unique(unlist(gene_df))
gene_df <- rbind(data.frame(parent="",child=feats[!feats%in%gene_df$child]),gene_df)

gene_df$prefix <- NA
gene_df$name <- NA

#For each unique parent, find associated children and assign prefix
for (ip in unique(gene_df$parent)){
  match_indx = which(gene_df$parent==ip)
  gene_df$prefix[match_indx] <- 10^c(seq(0,length(match_indx)-1))
}

gene_df$name[gene_df$parent==""]=gene_df$prefix[gene_df$parent==""]

#Assign names recursively
while (sum(is.na(gene_df$name))>0){
  parent_names <- gene_df$name[match(gene_df$parent,gene_df$child)]
  sel = (is.na(gene_df$name) & !is.na(parent_names))
  gene_df$name[sel] = paste0(gene_df$prefix[sel],parent_names[sel])
}

print(gene_df)

#Check uniqueness
print(length(unique(gene_df$name))==dim(gene_df)[1])