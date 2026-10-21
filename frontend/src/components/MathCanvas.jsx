// React component that will contain the Excalidraw math workspace.
import {Tldraw, useEditor, TldrawUiButton, toRichText, DefaultToolbar, DefaultToolbarContent} from 'tldraw'
import 'tldraw/tldraw.css'
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import { useState } from 'react';
import { Vision } from '../api';



export default function WhiteBoard(){
    const [image, setImage] = useState("");
    const [AIOutput, setAIOutput] = useState("");
    
    function ImageButton() {
        
        const editor = useEditor();
        
        return <TldrawUiButton
                    type="primary"
                    style={{ alignSelf: 'center', paddingLeft:'10px', paddingRight:'10px', color:'#459381'}}
                    onClick={async () => {
                        try{
                            const shapeIds = editor.getCurrentPageShapeIds();
                            if (shapeIds.size === 0) return alert('No shapes on the canvas')
                            const { blob } = await editor.toImage([...shapeIds], { format: 'png', background: false });
                            const response = await Vision(blob);
                            console.log(response);
                            setAIOutput(response);

                        }catch{
                            const shapeIds = editor.getCurrentPageShapeIds();
                            if (shapeIds.size === 0) return alert('No shapes on the canvas')
                            const { blob } = await editor.toImage([...shapeIds], { format: 'png', background: false });
                            const response = await Vision(blob);
                            console.log(response);
                            setAIOutput(response);
                        }
                        
                        
                    }}>
                    <AutoAwesomeIcon/> Sumbit Work
                </TldrawUiButton>
    }

    function CustomToolbar() {
        return (
            <DefaultToolbar>
                <ImageButton/>
                <DefaultToolbarContent/>
            </DefaultToolbar>
        );
    }

    
    const allowedTools = new Set([
        'select',    // Cursor; also selects and moves shapes
        'hand',      // Drag to pan the canvas
        'draw',
        'arrow',
        'rectangle',
        'eraser',
        'ellipse',
        'line'
    ]);

    const overrides = {
        tools(_editor, tools) {
            return Object.fromEntries(
                Object.entries(tools).filter(([id]) => allowedTools.has(id))
            );
        },
    };

    return <div style={{ position: 'fixed', inset:0}}>
        <Tldraw overrides={overrides} components={{Toolbar:CustomToolbar}}/>
    </div>
}