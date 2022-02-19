print("smit")self. left
= left
#
self.right = right
class Solution:
def dfs(self, node):
    if not node:
        return 0
    if not node. left and not node. right:
        return 1
    left, right = self.dfs(node.left), self.dfs(node.right)
#print(left, right)
    if left == 1 or right == 1:
        self.ans += 1
    return -1
    if left == -1 or right == -1:
        return 0
    if left == 0 and right == 0:
        return 1