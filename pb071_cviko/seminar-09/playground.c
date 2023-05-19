#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "stack.h"
#include "tree.h"
#include "limits.h"
#include "assert.h"

#define UNUSED(x) (void) (x)

/**********
 * Task 1 *
 ******** */

int tree_sum(const struct node *node) {
    if (node == NULL)
        return 0;
    return node->value + tree_sum(node->left) + tree_sum(node->right);
}

int tree_size(const struct node *node) {
    if (node == NULL)
        return 0;
    return 1 + tree_size(node->left) + tree_size(node->right);
}

int tree_max_value(const struct node *node) {
    assert(node != NULL);
    int left;
    int right;
    if (node->left == NULL && node->right == NULL)
        return node->value;

    if (node->left == NULL) {
        right = tree_max_value(node->right);
        return (node->value > right) ? (node->value) : (right);
    }
    if (node->right == NULL) {
        left = tree_max_value(node->left);
        return (node->value > left) ? (node->value) : (left);
    }

    left = tree_max_value(node->left);
    right = tree_max_value(node->right);
    int biggest = (left > right) ? (left) : (right);
    int res = (node->value > biggest) ? (node->value) : (biggest);
    return res;
}

void usage_task_1(const struct tree *tree) {
    puts("Task 1");
    if (tree == NULL || tree->root == NULL) {
        fprintf(stderr, "\tthe tree is empty");
        return;
    }

    printf("\tsum: %d\n", tree_sum(tree->root));
    printf("\tsize: %d\n", tree_size(tree->root));
    printf("\tmax number: %d\n", tree_max_value(tree->root));
}

/* small main */
int projector_sum(int value) {
    return value;
}

#define UNUSED(x) (void)(x)  // Hello old friend, ...

int projector_size(int value) {
    UNUSED(value);
    return 1;
}

int is_dividable_by_3(int value) {
    return (value % 3 == 0) ? 1 : 0;
}

int parne(int val) {
    return (val % 2 == 0) ? 1 : 0;
}

int tree_aggregate(const struct node *node, int (*projector)(int)) {
    if (node == NULL)
        return 0;
    return projector(node->value) + tree_aggregate(node->left, projector) + tree_aggregate(node->right, projector);
}

void operation_sum(int value, void *data_pack) {
    int *partial_result = (int *) data_pack;
    *partial_result += value;
}

void minimax(int val, int arr[2]){
    if (val < arr[1])
        arr[1] = val;
    if (val > arr[2])
        arr[2] = val;
}
void inbetweenus(int val, int arr[3]){
    if (val > arr[0] && val < arr[1])
        arr[2] += 1;
}
struct my_arr{
    int length;
    int *array;
};
void sequence(int val, struct my_arr *arr){
    arr->length +=1;
    arr->array = realloc(arr->array, sizeof (int) * arr->length);
    arr->array[arr->length -1] = val;
}

void tree_for_each(const struct node *node, void (*operation)(int, void *), void *data_pack) {
    if (node == NULL)
        return;
    operation(node->value, data_pack);
    tree_for_each(node->left, operation, data_pack);
    tree_for_each(node->right, operation, data_pack);
}

int get_tree_sum(const struct tree *tree) {
    int result = 0;
    if (tree && tree->root) {
        tree_for_each(tree->root, &operation_sum, &result);
    }
    return result;
}
int[2] tree_min_max(const struct tree *tree) {
    int result = {tree->root->value, tree->root->value};
    if (tree && tree->root) {
        tree_for_each(tree->root, &minimax, &result);
    }
    return result;
}
int tree_seq(const struct tree *tree) {
    int result = 0;
    if (tree && tree->root) {
        tree_for_each(tree->root, &sequence, &result);
    }
    return result;
}

int main(void) {
    srand(time(NULL)); // initialize pseudo-random generator
    struct tree *tree = tree_create(11);
    if (tree == NULL)
        return EXIT_FAILURE;

    if (!tree_print(tree, stdout)) {
        tree_destroy(tree);
        return EXIT_FAILURE;
    }

    int exit_status = EXIT_SUCCESS;
    // HERE YOU CAN USE THE GENERATED TREE
    usage_task_1(tree);

    tree_destroy(tree);

    return exit_status;
}
