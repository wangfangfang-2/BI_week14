##Thinking1	常用的路径规划算法有哪些?			简要说出常用的路径规划算法（10points）
Dijkstra 算法；Floyd 算法；蚁群算法；Lee 算法；双向搜索算法

##Thinking2	推荐系统的架构是怎样的？			简要说明推荐系统的架构（10points）
推荐系统是一种 信息过滤 系统，根据用户的历史行为、社交关系、兴趣点等推荐给他们喜欢等商品，其中算法可以判断用户当前感兴趣的物品或内容。也可以将它理解为一家为每个个体而开的商店。店铺里摆放的都是需要的，或者适合的商品。它和搜索最大的区别是，搜索是主动式的，根据关键词和引擎参数、搜索引擎召回、机器学习排序，决定给你看到的是哪些内容。推荐系统目标很多，需要结合场景来定。
推荐系统中的EE问题：即利用与探索。前者充分利用已有的资源，但可能存在信息茧房。后者是认知未知的世界，但准确率可能低。在没有大量数据的情况下，需要探索。
推荐系统的3个模块：A数据源，B召回，C排序A 数据源是item特征，用户画像，用户行为。B 召回是粗筛的阶段，可以得到候选物品集。C 排序阶段通过对多个召回通道的内容进行打分排序，选出最优的少量结果。兼顾推荐系统的多维度指标：覆盖率，多样性，新颖度。
召回和排序；基于内容的推荐和基于协同过滤的推荐。
协同过滤：基于邻域的和基于模型的。
基于模型的算法：MF PMF BPMF
FM Factorization Machine(因子分解机)用于在在高度稀疏的数据场景下如推荐系统。

##Thinking3	你都了解推荐系统中的哪些常用算法？原理是怎样的？			简要说明常用的推荐系统算法及原理（10points）
基于内容的推荐（内容特征表示；特征学习，推荐列表），是静态的物理属性。基于协同过滤的推荐（群体智能，用户历史行为），是动态的属性。基于关联规则的推荐，比如Apriori算法；FP-growth算法。基于效用的推荐。基于知识的推荐。基于组合的推荐（实际工作中经常采用，可以根据每种推荐算法适用的使用场景综合考虑）。	
关联规则：从大规模数据集中寻找物品间的隐含关系			
原理	Apriori算法的流程是怎样的：k=1,计算k项集的支持度；筛选掉小于最小支持度的项集；如果项集为空，对应k-1项集的结果为最终结果，否则k=k+1,重复以上步骤。			
原理	Apriori算法存在哪些不足：不能计算提升度等，内容不详细。且计算的时间复杂度高。	可能产生大量的候选集，每次计算都需要重新扫描数据集，计算每个项集的支持度，浪费了计算时间和空间。		
FM算法：每个特征只有一个隐向量，FM是FFM的特例。FFM算法：计算粒度更细，计算更慢。每个特征有多个隐向量，使用哪个，取决于和哪个向量进行点乘，通过引入field的概念，FFM把相同性质的特征归于同一个field。隐向量的长度为 k，FFM的二次参数有 nfk 个，多于FM模型的 nk 个.由于隐向量与field相关，FFM二次项并不能够化简，计算复杂度是O(k*n^2)FFM的k值一般远小于FM的k值
eep模型:原始特征向量维度非常大，高度稀疏，为了更好的发挥DNN模型学习高阶特征的能力，设计子网络结构（从输入层=>嵌入层），将原始的稀疏表示特征映射为稠密的特征向量。Input Layer => Embedding Layer,不同field特征长度不同，但是子网络输出的向量具有相同维度k;利用FM模型的隐特征向量V作为网络权重初始化来获得子网络输出向量.在推荐系统中，对于离线变量我们需要转换成one-hot => 维度非常高，可以将其转换为embedding向量,原来每个Field i维度很高，都统一降成k维embedding向量.方法：接入全连接层，对于每个Field只有一个位置为1，其余为0，因此得到的embedding. FM模型和Deep模型中的子网络权重共享，也就是对于同一个特征，向量Vi是相同的. DeepFM中的模块：Sparse Features，输入多个稀疏特征；Dense Embeddings：对每个稀疏特征做embedding，学习到他们的embedding向量(维度相等，均为k），因为需要将这些embedding向量送到FM层做内积。同时embedding进行了降维，更好发挥Deep Layer的高阶特征学习能力。FM Layer：一阶特征：原始特征相加，二阶特征：原始特征embedding后的embedding向量两两内积；Deep Layer，将每个embedding向量做级联，然后做多层的全连接，学习更深的特征；Output Units，将FM层输出与Deep层输出进行级联，接一个dense层，作为最终输出结果。

##Thinking4	我们在课上讲解过常用的机器学习，深度学习模型，推荐系统算法，以及启发式算法，路径规划原理等，针对这些模块，请你针对其中一个进行思维导图梳理			能对课上讲过的某一模块进行思维导图梳理（20points）


