
// 1.判断两个矩形是否重叠,两个矩形只能沿着与X、Y轴平行方向移动

struct Rectangle
{
  // Coordinates of bottom left corner
  int x, y;
  int height, width;
};

// 算法：
// 经过分析得出结论：
// 两个矩形重叠的条件是其中一个矩形至少有一个顶点落在另一个矩形的内部
// 且只需要判断一个矩形有点在另一个的内部，此时意味着另一个矩形的顶点也在这个矩形的内部

bool RectanglesOverlap(const Rectangle &r1, const Rectangle &r2)
{
  // 第一个矩形的顶点
  std::pair<int, int> pt11,pt12,pt13,pt14;
  // 第二个矩形的顶点
  std::pair<int, int> pt11,pt12,pt13,pt14;

  pt11.first = r1.x;
  pt11.second = r1.y;

  pt12.first = r1.x;
  pt12.second = r1.y + r1.height;

  pt13.first = r1.x + r1.width;
  pt13.second = r1.y + r1.height;

  pt14.first = r1.x + r1.width;
  pt14.second = r1.y;

  // 判断r1的顶点是否落在r2内部, r1顶点在r2内部就意味着r2的顶点也在r1内部
  if ((pt11.first >= r2.x) &&
      (pt11.first <= r2.x+r2.width) &&
      (pt11.second >= r2.y) &&
      (pt11.second <= r2.y+r2.height))
    {
      return true;
    }

  if ((pt12.first >= r2.x) &&
      (pt12.first <= r2.x+r2.width) &&
      (pt12.second >= r2.y) &&
      (pt12.second <= r2.y+r2.height))
    {
      return true;
    }

  if ((pt13.first >= r2.x) &&
      (pt13.first <= r2.x+r2.width) &&
      (pt13.second >= r2.y) &&
      (pt13.second <= r2.y+r2.height))
    {
      return true;
    }

  if ((pt14.first >= r2.x) &&
      (pt14.first <= r2.x+r2.width) &&
      (pt14.second >= r2.y) &&
      (pt14.second <= r2.y+r2.height))
    {
      return true;
    }

  return false;
}

//2.从左边到右打印第n层的二叉树节点的信息

struct TreeNode
{
  int value;
  TreeNode *leftChild;
  TreeNode *rightChild;
  TreeNode *parent;
};

// 算法：
// 使用递归的方式，利用层级计数器确定指定层的数据并打印出来

void PrintTreeLevel(const TreeNode *root, int depth)
{
  // 当递归到指定层时停止继续向更深的层次递归
  bool bStop = false;

  // 层级计数器
  static int counter = 0;

  if (depth == counter++)
    {
      printf("%d", root->value);
      bStop = true;

      // 往回递归的时候，层级需要递减
      counter--;
    }

  if (!bStop)
    {
      PrintTreeLevel(root->leftChild);
      PrintTreeLevel(root->rightChild);

      // 往回递归的时候，层级需要递减
      counter--;
    }
}

//3.返回单链表中倒数第5个值

// define single list
struct _Node
{
  int     data;
  _Node * next;
};
typedef struct _Node Node, * PNode;

// 算法:
// 利用递归函数栈的LIFO的性质，在递归到最深层次后，往回递归的时候进行计数
// 并返回指定序号的元素

// 辅助函数用于创建链表
// create single list with same order as array's
PNode CreateSingleList(int *array, int n)
{
  PNode head, pre;
  head = pre = NULL;
  
  for(int i = 0; i < n; ++i)
  {
    Node* pNode = new Node();
    pNode->data = array[i];

    // head Node
    if(NULL == pre)
    {
      pre = pNode;
      head = pNode;
    }
    else
    {
      pre->next = pNode;
      pre = pNode;
    }
  }

  // tail Node
  if(NULL != pre)
    pre->next = NULL;
  
  return head;
}

// 返回单链表倒数第5个值
int  n5thElement = 0;
void Return5thElement(PNode root)
{
  if (NULL == root)
    return;

  Return5thElement(root->next);

  static int counter = 0;

  if (5 == ++counter)
  {
      n5thElement = root->data;
  }        
}

int main(void)
{
  // 创建链表
  // Single list
  int list[10] = {1,2,3,4,5,6,7,8,9,10};
  PNode head = CreateSingleList(list, 10);

  // 返回第5个元素
  Return5thElement(new_head);
  cout << "第5个元素是" << n5thElement << std::endl;
}

// test case 

list 内容      期望值        实际值

1,2,3,4,5,6   2             2
6,5,4,3,2,1   5             5
0,5,4,7,8,6,9 4             4


					  
