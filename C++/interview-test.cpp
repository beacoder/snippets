
// 1.判断两个矩形是否重叠,两个矩形只能沿着与X、Y轴平行方向移动

struct Rectangle
{
  // upper and left corner
  int x1, y1;
  
  // right and down corner
  int x2, y2;
};

// 算法：
// see @http://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other
// A与B不相交的情况包括四种情况:
// Cond1. If A's left edge is to the right of the B's right edge, - then A is Totally to right Of B
// Cond2. If A's right edge is to the left of the B's left edge, - then A is Totally to left Of B
// Cond3. If A's top edge is below B's bottom edge, - then A is Totally below B
// Cond4. If A's bottom edge is above B's top edge, - then A is Totally above B

// A与B相交需要满足
// A's Left Edge to left of B's right edge, and
// A's right edge to right of B's left edge, and
// A's top above B's bottom, and
// A's bottom below B's Top

if (A.x1 < B.x2 && 
    A.x2 > B.x1 && 
    A.y1 < B.y2 && 
    A.y > B.y1) 
    {
    	A intersect with B.
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


					  
