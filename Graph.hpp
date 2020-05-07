/**
 * @author Ashwin K J
 * @file
 * Graph Class: Graph Data-structure
 */
#ifndef GRAPH_H
#define GRAPH_H

/* #include "Graph_Function.hpp" */
#include <fstream>
#include <iostream>
#include <list>
#include <llvm/IR/CallSite.h>
#include <llvm/IR/DebugInfoMetadata.h>
#include <llvm/IR/InstrTypes.h>
#include <llvm/IR/Intrinsics.h>
#include <regex>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>
#include <boost/graph/depth_first_search.hpp>
#include <map>
using namespace boost;

namespace hydrogen_framework {
/* Forward declaration */
class Graph_Edge;
class Graph_Function;
class Graph_Instruction;
class Graph_Line;
class Path;


/**
 * Graph Class: Class for generating Graphs
 */
class Graph {
public:
  /**
   * Constructor
   * Initialize ID to zero
   */
  Graph(unsigned ver)
      : graphID(0), graphVersion(ver), graphEntryID(std::numeric_limits<unsigned int>::max() - 1),
        graphExitID(std::numeric_limits<unsigned int>::max() - 2) {
    whiteList.push_back("__isoc99_scanf");
    whiteList.push_back("printf");
    whiteList.push_back("malloc");
    whiteList.push_back("strlen");
    whiteList.push_back("strcpy");
    whiteList.push_back("strcmp");
    whiteList.push_back("free");
    whiteList.push_back("getpwnam");
    whiteList.push_back("__ctype_b_loc");
    whiteList.push_back("tolower");
    whiteList.push_back("setpwent");
    whiteList.push_back("getpwent");
    whiteList.push_back("strchr");
    whiteList.push_back("strcasecmp");
    whiteList.push_back("perror");
    whiteList.push_back("toupper");
    whiteList.push_back("malloc");
    whiteList.push_back("strlen");
    whiteList.push_back("strcpy");
    whiteList.push_back("strcmp");
    whiteList.push_back("free");
    whiteList.push_back("getpwnam");
    whiteList.push_back("__ctype_b_loc");
    whiteList.push_back("tolower");
    whiteList.push_back("setpwent");
    whiteList.push_back("getpwent");
    whiteList.push_back("strchr");
    whiteList.push_back("strcasecmp");
    whiteList.push_back("perror");
    whiteList.push_back("snprintf");
    whiteList.push_back("toupper");
  }

  /**
   * Destructor
   */
  ~Graph() {
    graphEdges.clear();
    graphFunctions.clear();
  }

  /**
   * Get next ID
   */
  unsigned getNextID() { return ++graphID; }

  /**
   * Return graphVersion
   */
  unsigned getGraphVersion() { return graphVersion; }

  /**
   * Set graphVersion
   */
  void setGraphVersion(unsigned ver) { graphVersion = ver; }

  /**
   * Push Graph_Edge into graphEdges
   */
  void pushGraphEdges(Graph_Edge *edge) { graphEdges.push_back(edge); }

  /**
   * Push Graph_Function into graphFunctions
   */
  void pushGraphFunction(Graph_Function *func);

  /**
   * Add sequential edges for the instructions in a Graph_Line
   */
  void addSeqEdges(Graph_Line *line);

  /**
   * Add branch type edges for ICFG
   */
  void addBranchEdges();

  /**
   * Add virtual nodes and corresponding edges to the Graph_Function
   */
  void addVirtualNodes(Graph_Function *func);

  /**
   * Add function call edges
   * Call only after addVirtualNodes
   */
  void addFunctionCallEdges();

  /**
   * Function to add Graph_Edge to both graphEdges and corresponding Graph_Instruction
   */
  void addEdge(Graph_Instruction *from, Graph_Instruction *to, Graph_Edge *edge);

  /**
   * Print the graph in DOT format
   */
  void printGraph(std::string graphName);

  /////////////////////////////////////////  
  std::tuple<std::vector<Path>*, std::vector<Path>*>  dfs();

  void dfsHelper(Path* currentPath, Graph_Instruction* funcExit);
  
  void path_added();

  void path_removed();

  //////////////////////////////////////////

  /**
   * Find matching instruction in the ICFG
   * Can return NULL if no match is found
   */
  Graph_Instruction *findMatchedInstruction(llvm::Instruction *matchInst);

  /**
   * Find virtual entry for the given function name
   * Can return NULL if no match is found
   */
  Graph_Instruction *findVirtualEntry(std::string funcName);

  /**
   * Find virtual entry for the given function name
   * Can return NULL if no match is found
   */
  Graph_Instruction *findVirtualExit(std::string funcName);

  /**
   * Return graphFunctions
   */
  std::list<Graph_Function *> getGraphFunctions() { return graphFunctions; }

  /**
   * Return TRUE if it is a virtual node
   */
  bool isVirtualNodeLineNumber(unsigned lineNumber);

  /**
   * Return graphEdges
   */
  std::list<Graph_Edge *> getGraphEdges() { return graphEdges; }

  /**
   * Return whiteList
   */
  std::list<std::string> getWhiteList() { return whiteList; }

private:
  unsigned graphID;                           /**< Unique Graph ID */
  unsigned graphVersion;                      /**< Version of graph. */
  unsigned graphEntryID;                      /**< ID for all virtual entry Node. Set to max -1 */
  unsigned graphExitID;                       /**< ID for all virtual exit Node. Set to max -2 */
  std::list<Graph_Edge *> graphEdges;         /**< Container for Edges in the graph */
  std::list<Graph_Function *> graphFunctions; /**< Container for function containers */
  std::list<std::string> whiteList;           /**< Container for white-listed functions */
  std::vector<Path> newlyAdded;
  std::vector<Path> newlyRemoved;
};                                            // End Graph Class

class Path{
  public:
    Path(unsigned ver){
      totalVersions=ver;
      for(unsigned i=1; i<= ver; i++){
        verCount[i]=0;
      }

      ac= new bool [totalVersions];
      ewo = new bool [totalVersions];
    }

    Path(const Path &obj){
      verCount=obj.verCount;
      instructions=obj.instructions;
      
      // allocate and copy content
      ac= new bool [totalVersions];
      ewo = new bool [totalVersions];
      *ac=*obj.ac;
      *ewo=*obj.ewo;
    }

    ~Path(){
        delete ac;
        delete ewo;
    }
  
    std::vector<unsigned> allContains();
    std::vector<unsigned> existsWithout();

    bool* allContainsBool();
    bool* existsWithoutBool();
    std::vector<Graph_Instruction*> instructions;

    bool added=false;
    bool removed=false;
    unsigned arVersion=0;
    unsigned totalVersions;
    std::map<unsigned, unsigned> verCount;

  private:
    bool *ac;
    bool *ewo;
};

/**
 * Find the line number and file name of the given LLVM instruction
 * Will return 0 if no information found
 */
void getLocationInfo(llvm::Instruction &I, unsigned int &DILocLine, std::string &DIFile);
} // namespace hydrogen_framework
#endif

