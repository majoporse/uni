#define CUT
#define CUT_MAIN
#ifndef DEBUG
#  define CUT_FORK_MODE
#endif

#include "cut.h"

#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "queue.h"

//=============================================================================
//  Examples
//=============================================================================

/*
 * Trivial test that succeeds.
 */
TEST(trivial_success) {
    int zero = 0;
    CHECK(zero == 0);
}

/*
 * Trivial test that fails.
 */
TEST(trivial_failure) {
    int zero = 0;
    CHECK(zero == 1);
}

//-----------------------------------------------------------------------------

/*
 * Example of ‹queue_create()› test.
 *
 * Scenario
 * --------
 * WHEN     ‹queue_create()› gets called
 * WHEN     requested capacity is zero
 * THEN     queue is created successfully
 */
TEST(queue_create__zero_capacity) {
    struct queue *queue = NULL;
    // The ‹queue_create()› should succeed.
    CHECK(queue_create(&queue, sizeof(int), 0u));

    // ‹queue› should now point to allocated structure.
    CHECK(queue != NULL);

    // Attributes should be set properly.
    CHECK(queue->element == sizeof(int));
    CHECK(queue->capacity == 0u);
    CHECK(queue->index == 0u);
    CHECK(queue->size == 0u);
    // ‹queue.memory› may or may not be ‹NULL›, the documentation does not
    // specify this.

    // Well done, free the structure.
    free(queue);
    // We didn't use ‹queue_destroy()› since we are supposed to call only
    // one function from the queue interface in each test. If we did call
    // it, we would risk having two sources of failure in one test.
}

/**
 * Example of ‹queue_enqueue()› test.
 *
 * Scenario
 * --------
 * GIVEN    empty queue of integers with capacity 32
 * WHEN     a single element is enqueued
 * THEN     size changes to 1
 */
TEST(queue_enqueue__single) {
    int memory[32u]; // This simulates queue's internal memory.
    struct queue queue = {
            // We will set up the structure ourselves instead of calling
            // ‹queue_create()›, since we are not (yet) sure it works as it should.
            .element    = sizeof(*memory),
            .capacity   = sizeof(memory) / sizeof(*memory),
            .memory     = memory,
            // All other attributes not mentioned here will
            // be initialized to 0.
    };

    // Now let's enqueue a single element.
    int number = 123456;
    // The function shall not fail.
    CHECK(queue_enqueue(&queue, &number));

    // Check that the element was indeed stored in the memory.
    CHECK(memory[0] == number);
    // Make sure that size has increased.
    CHECK(queue.size == 1u);
    // Index should remain 0.
    CHECK(queue.index == 0u);
}

//=============================================================================
//  Your tests go here
//=============================================================================

TEST(queue_element_size) {
    struct queue test;
    test.element = sizeof(int);

    CHECK(sizeof(int) == queue_element_size(&test));
}
TEST(queue_element_size_empty){
    struct queue test = {0,0,0,0,NULL};
    CHECK(0 == queue_element_size(&test));

}

TEST(queue_capacity) {
    struct queue test;
    test.capacity = 10;

    CHECK(10 == queue_capacity(&test));
}

TEST(queue_peek){
    struct queue test;
}