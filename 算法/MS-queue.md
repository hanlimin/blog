### non-blockingconcurrent queue

```c
structure pointer t f ptr: pointer to node t, count: unsignedinteger g
structure node t f value: data type, next: pointer t g
structure queue t f Head: pointer t, Tail: pointer t g

initialize(Q: pointer to queue t)
    node = new node() 
    node–>next.ptr = NULL 
    Q–>Head = Q–>Tail = node 
    
enqueue(Q: pointer to queue t, value: data type)
    node = new node()
    node–>value = value
    node–>next.ptr = NULL

    loop
       /*先获得tail指针和最后一个节点的next*/
       tail = Q–>Tail
       next = tail.ptr–>next
       /*判断如果刚才获得的tail没有改变（即：其它线程没有改变增加节点进而tail指针*/
       if tail == Q–>Tail
         /*tail是否指向最后一个节点，如果没有变动，加入节点*/
           if next.ptr == NULL
               if CAS(&tail.ptr–>next, next, (node, next.count+1))
                  break
               endif
           else /*tail没有指向最后一个节点，即：其它线程在末尾增加了节点*/
               CAS(&Q–>Tail, tail, (next.ptr, tail.count+1))
           endif
        endif
     endloop
    /*loop操作在tail之后增加了节点，修改tail指向最后一个节点*/
    CAS(&Q–>Tail, tail, (node, tail.count+1))
               
dequeue(Q: pointer to queue t, pvalue: pointer to data type)
    loop
    		/*检查head,tail,next是否具有一致性*/
        head = Q–>Head
        tail = Q–>Tail
        next = head.ptr–>next
        /*如果head节点没有改变*/
        if head == Q–>Head
          /*如果head和tail都指向同一个节点*/
            if head.ptr == tail.ptr
            /*如果该节点的next为NULL，则队列为空，返回*/
                if next.ptr == NULL
                return FALSE
            endif
            /*此时next.ptr不为NULL，即有节点插入，而tail执行落后与新插入的节点，
              指向新加入的节点*/
            CAS(&Q–>Tail, tail, (next.ptr, tail.count+1))
          else
            /*如果不为空，则取得首个节点的数据，然后修改Head指针
             如果head不一致，则说明已经有其它线程进行了出队操作，
            重新loop开始*/
            *pvalue = next.ptr–>value
            if CAS(&Q–>Head, head, (next.ptr, head.count+1))
              break
            endif
          endif
        endif
    endloop
    free(head.ptr)
    return TRUE
```

### a two-lock concurrent queue.

```c
structure nodo_t 			{ value: data type, next: pointer to node_t}
structure queue_t 			{ Head: pointer to node_t, Tail: pointer to node_t, H_lock: lock type, T_lock: lock type }

initialize(Q: pointer to queue t)
    node = new node() 				 					# Allocate a free node
    node–>next.ptr = NULL 								# Make it the only node in the linked list
    Q–>Head = Q–>Tail = node 	  						# Both Head and Tail point to it
    Q–>H lock = Q–>T lock = FREE  						# Locksare initially free
    
enqueue(Q: pointer to queue t, value: data type)
    node = new node() 										 # Allocate a new node from the free list
    node–>value= value										# Copyenqueuedvalue into node
    node–>next.ptr = NULL 									# Set next pointer of node to NULL
    lock(&Q–>T lock) 										# Acquire T lock in order to accessTail
    	Q–>Tail–>next = node 								# Link node at the end of the linked list
    	Q–>Tail = node										 # Swing Tail to node
    unlock(&Q–>T lock) 										# ReleaseT lock
    
dequeue(Q: pointer to queue t, pvalue: pointer to data type): boolean
	lock(&Q–>H lock) 										  # Acquire H lock in order to accessHead
        node = Q–>Head 									  # Read Head
        new head = node–>next 							  # Read next pointer
			if new head == NULL # Is queueempty?
            unlock(&Q–>H lock) # ReleaseH lock before return
            return FALSE # Queuewas empty
        endif
        *pvalue = new head–>value 						  # Queuenot empty. Read value before release
        Q–>Head = new head 								  # Swing Head to next node
    unlock(&Q–>H lock) 										 # ReleaseH lock
    free(node) 												  # Free node
    return TRUE 											  # Queuewas not empty, dequeuesucceeded
```

