function remap-reload --wraps='keyd reload' --wraps='sudo keyd reload' --description 'alias remap-reload sudo keyd reload'
  sudo keyd reload $argv
        
end
