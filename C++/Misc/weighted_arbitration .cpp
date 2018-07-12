//@see https://blog.csdn.net/wzh200x/article/details/37708609
//
// 需求：广告按权重展现 => weighted arbitration
//
// 基本算法描述如下:
// 1、每个广告增加权重
// 2、将所有匹配广告的权重相加sum，
// 3、以相加结果为随机数的种子，生成 1~sum 之间的随机数 rd
// 4、接着遍历所有广告，访问顺序可以随意.
//    将当前节点的权重值加上前面访问的各节点权重值得到 curWt, 判断 curWt >= rd.
//    如果条件成立则返回当前节点, 如果不是则继续累加下一节点，直到符合上面的条件, 由于 rd<=sum，因此一定存在 curWt >= rd.

#include <algorithm>
#include <iostream>
#include <iterator>
#include <map>
#include <set>
#include <stdlib.h>
#include <time.h>

// Key, Value -> Weight
const std::map<uint32_t, uint32_t> pool {
    {1,1},
    {2,2},
    {3,3},
    {4,4}
};

// AccumulatedWeight
const std::set<uint32_t> accumulatedWeights {1, 3, 6, 10};

// AccumulatedWeight
std::map<uint32_t, uint32_t> accumulatedWeights2 {
    {1,1},
    {2,2},
    {3,3},
    {4,4}
};

std::map<uint32_t, std::vector<int> > finalResult;

uint32_t getSum()
{
    uint32_t sum = 0;

    for (const auto& pair : pool)
    {
        sum += pair.second;
    }

    return sum;
}

int main(int argc, char *argv[])
{
    // srand(getSum());
    srand (time(NULL));

    for (int i = 0; i < 100; ++i)
    {
        uint32_t curRd = rand() % getSum() + 1;

        int position = std::distance(accumulatedWeights.begin(),
                                     std::find_if(accumulatedWeights.begin(), accumulatedWeights.end(),
                                                  [curRd](uint32_t accumulatedWeight)
                                                  {
                                                      return curRd <= accumulatedWeight;
                                                  })
                                     );

        finalResult[position].emplace_back(i);

        // std::cout << "This one falls into position: " << position << std::endl;
    }
    
    /* This version has smaller fluctuation.
    uint32_t initRd = rand();
    uint32_t currentIndex = 1;

    for (int i = 0; i < 10000; ++i)
    {
        uint32_t curRd = initRd % getSum();
                                     
        if (curRd <= accumulatedWeights2[currentIndex])
        {
            currentIndex = (curRd == 0 ? 0 : currentIndex);
        }
        else
        {
            currentIndex = ((currentIndex + 1) % pool.size());
        }
        
        finalResult[currentIndex-1].emplace_back(i);
        
        initRd += 1;

        //std::cout << "This one falls into position: " << currentIndex -1 << std::endl;
    }
    */

    for (const auto& pair : finalResult)
    {
        std::cout << "Pool-" << pair.first << " contains " << pair.second.size() << " elements." << std::endl;
    }

    return 0;
}
