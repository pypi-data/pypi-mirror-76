def intesort(nums=[], ascend = True):

    """
    :param nums:
    :param ascend:
    :return nums
    This is a number's list sorting function which will sort the numbers either in ascending order or descending order
    """

    # if no list then return empty array
    if nums == None:
        return []

    for i in range(0, len(nums)):
        for j in range(i, len(nums)):

            """ if ascending is true then used the first solution or else used the second one"""
            if(ascend == True):
                if(nums[i] > nums[j]):
                    switct_element(i, j, nums)
            else:
                if (nums[i] < nums[j]):
                    switct_element(i, j, nums)

    return nums

def switct_element(i, j, nums):
    """
    switch the elements within number list
    :param i:
    :param j:
    :param nums:
    :return:
    """
    temp = nums[i]
    nums[i] = nums[j]
    nums[j] = temp