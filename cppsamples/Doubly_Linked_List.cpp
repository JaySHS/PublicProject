#include <iostream>

class Node{
    public:
        int data;
        Node* previous;
        Node* next;

        Node(){data = 0; previous = NULL; next = NULL;}
        Node(int d){this->data = d; this->previous = NULL; this->next = NULL;}
};

class LList{
    Node* head;
    Node* tail;

    public:
        int length = 0;
        LList(){head = NULL;}
        Node* isearch(int);
        Node* search(int);
        Node* rsearch(int);
        void push(int);
        void append(int);
        void print(int);
        void printall();
        void remove(int);
        
};

Node* LList::isearch(int node_index){
    if(node_index < (length/2)){
        return search(node_index);
    }
    else{
        return rsearch(length-node_index-1);
    }
}

Node* LList::search(int node_index){
    Node* index = head;
    if(length <= node_index){
        std::cout << "Error : index out of length" << std::endl;
        return NULL;
    }
    while(node_index-- > 0){index = index->next;}
    return index;
}

Node* LList::rsearch(int node_index){
    Node* index = tail;
    if(length <= node_index){
        std::cout << "Error : index out of length" << std::endl;
        return NULL;
    }
    while(node_index-- > 0){index = index->previous;}
    return index;
}

void LList::push(int new_data){
    Node* newnode = new Node(new_data);
    if(head == NULL){tail = newnode;}
    else{head->previous = newnode;}
    newnode->next = head;
    head = newnode;
    length++;
}

void LList::append(int new_data){
    Node* newnode = new Node(new_data);
    if(head == NULL){head = newnode;}
    else{tail->next = newnode;}
    newnode->previous = tail;
    tail = newnode;
    length++;
}

void LList::print(int node_index){
    if(length <= node_index){
        std::cout << "Error : index out of length" << std::endl;
        return;
    }
    Node* target = isearch(node_index);
    std::cout << "data in Node #" << node_index << " is: " << target->data << std::endl;
}

void LList::printall(){
    for(int i = 0; i < length; i++){
        print(i);
    }
}

void LList::remove(int node_index){
    if(length <= node_index){
        std::cout << "Error : index out of length" << std::endl;
        return;
    }
    Node* target = isearch(node_index);
    if(target == head){head = head->next;}
    else if(target == tail){tail = tail->previous;}
    else{
        target->previous->next = target->next;
        target->next->previous = target->previous;
    }
    delete target;
    length--;
}

int main(){
    LList list;
    list.append(1);
    list.push(3);
    list.push(7);
    list.append(6);
    list.print(3);
    return 0;
}