/* canonfile.c -- read graphs (one per line, edges written as "(a,b,c)" anywhere on the line), print for each:
   n m aut canonical-edge-list.  Vertex set = union of edges, relabelled increasingly first (all files use 0..n-1). */
#include "refcanon.h"
#include <ctype.h>
int main(void){ char line[8192];
  while(fgets(line,sizeof line,stdin)){
    HG g; g.m=0; g.n=0; int maxv=-1; char *p=line;
    while((p=strchr(p,'('))){ int a,b,c; if(sscanf(p,"(%d,%d,%d)",&a,&b,&c)==3){ g.e[g.m++]=(uint16_t)((1u<<a)|(1u<<b)|(1u<<c)); if(a>maxv)maxv=a; if(b>maxv)maxv=b; if(c>maxv)maxv=c; } p++; }
    if(g.m==0) continue;
    g.n=maxv+1; HG c; long long au=canon(&g,&c);
    printf("n=%d m=%d aut=%lld :",g.n,g.m,au); for(int i=0;i<c.m;i++) printf(" %u",c.e[i]); printf("\n"); }
  return 0; }
