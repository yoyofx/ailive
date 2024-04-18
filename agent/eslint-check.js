module.exports = {
    meta: {
        type: "problem",
        docs: {
            description: "域名不能定义为常量."
        },
        fixable: "code",
        schema: []
    },
    create(context) {
        return {

            // Performs action in the function on every variable declarator
            VariableDeclarator(node) {
                // Check if a `const` variable declaration
                if (node.init && node.init.type === "TemplateLiteral" ) {
                    for (let i = 0; i < node.init.quasis.length; i++) {
                        const httpRegex = /^https?:\/\//i;
                        if (httpRegex.test(node.init.quasis[i].value.raw)) {
                            context.report({
                                node:node.init,
                                message: '域名不能定义为常量/变量. Unexpected value: {{ data }}.',
                                data: {
                                    data: node.init.quasis[i].value.raw
                                },
                                fix(fixer) {
                                    return fixer.replaceText(node.init, '""');
                                }
                            });
                        }
                    }
                }



                if (node.init && node.init.type === "BinaryExpression" ) {
                    // console.log(node)
                    if (node.init.left && node.init.left.type === "Literal" ) {

                        // // node.init.value to regex http scheme
                        const httpRegex = /^https?:\/\//i;
                        if (httpRegex.test(node.init.left.value)) {
                            context.report({
                                node:node.init,
                                message: '域名不能定义为常量/变量. Unexpected value: {{ data }}.',
                                data: {
                                    data: node.init.left.value
                                },
                                fix(fixer) {
                                    return fixer.replaceText(node.init, '""');
                                }
                            });
                        }
                
                        
                    }
                }


                // Check if value of variable is "bar"
                if (node.init && node.init.type === "Literal" ) {

                    // node.init.value to regex http scheme
                    const httpRegex = /^https?:\/\//i;
                    if (httpRegex.test(node.init.value)) {
                        context.report({
                            node,
                            message: '域名不能定义为常量/变量. Unexpected value: {{ data }}.',
                            data: {
                                data: node.init.value
                            },
                            fix(fixer) {
                                return fixer.replaceText(node.init, '""');
                            }
                        });
                    }

                    
                }
     
            }
        };
    }
};
